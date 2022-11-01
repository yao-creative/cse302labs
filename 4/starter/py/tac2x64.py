import json, sys, os
from typing import List

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

class tac2x64:
    def __init__(self, functn: str, tac_instrs: List) -> None:
        self.__tac_instr: List = tac_instrs
        self.__func_name: str = functn
        self.__assembly: List = []
        self.__temp_map: dict = {}

    # ---------------------------------------------------------------------#
    # Class Macro Variables
    # ---------------------------------------------------------------------#

    # idea reffered from lab1
    __binops={'add': 'addq',
              'sub': 'subq',
              'mul': (lambda ra, rb, rd: [f'\tmovq {ra}, %rax',
                                          f'\timulq {rb}',
                                          f'\tmovq %rax, {rd}']),
              'div': (lambda ra, rb, rd: [f'\tmovq {ra}, %rax',
                                          f'\tcqto',
                                          f'\tidivq {rb}',
                                          f'\tmovq %rax, {rd}']),
              'mod': (lambda ra, rb, rd: [f'\tmovq {ra}, %rax',
                                          f'\tcqto',
                                          f'\tidivq {rb}',
                                          f'\tmovq %rdx, {rd}']),
              'and': 'andq',
              'or': 'orq',
              'xor': 'xorq',
              'shl': (lambda ra, rb, rd: [f'\tmovq {ra}, %r11',
                                          f'\tmovq {rb}, %rcx',
                                          f'\tsalq %cl, %r11',
                                          f'\tmovq %r11, {rd}']),
              'shr': (lambda ra, rb, rd: [f'\tmovq {ra}, %r11',
                                          f'\tmovq {rb}, %rcx',
                                          f'\tsarq %cl, %r11',
                                          f'\tmovq %r11, {rd}'])}
    __unops = {'neg': 'negq',
               'not': 'notq'}

    __jcc = ["je", "jz",        # Src2 == Src1
           "jne", "jnz",      # Src2 != Src1
           "jl", "jnge",      # Src2 < Src1
           "jle", "jng",      # Src2 <= Src1
           "jg", "jnle",      # Src2 > Src1
           "jge", "jnl",      # Src2 >= Src1
           ]

    # ---------------------------------------------------------------------#
    # misc functions
    # ---------------------------------------------------------------------#

    def __lookup_temp(self, temp: str, instr: dict) -> str:
        """ Returns the value of the temp from the stack 
            while simultaneously creating a hash table """
        self.__assert_temporary(temp, instr)
        
        if temp in self.__temp_map:     # if temporary already exists return its value
            return self.__temp_map[temp]
        
        else:      # add a new destination for it considering there is one address for rsp
            self.__temp_map[temp] = f'{-8 * (len(self.__temp_map) + 1)}(%rbp)'
        
        return self.__temp_map[temp]

    def __add_instr_comment(self, instr: dict) -> None:
        """ Adds instruction as a comment in the assembly """

        if instr['result'] == None:
            if instr['opcode'] == 'jmp' or instr['opcode'] == 'print':
                self.__assembly.append(f'\t/*   {instr["opcode"]} {instr["args"][0]} [TAC] */')
            elif instr['opcode'] in self.__jcc:
                self.__assembly.append(f'\t/*   {instr["opcode"]} {instr["args"][0]}, {instr["args"][1]} [TAC] */')
            elif instr['opcode'] == 'label':
                self.__assembly.append(f'\t/*  {instr["args"][0]}: [TAC] */')
        
        elif len(instr["args"]) == 1:
            self.__assembly.append(f'\t/*   {instr["result"]} = {instr["opcode"]} {instr["args"][0]} [TAC] */')
        elif len(instr["args"]) == 2:
            self.__assembly.append(f'\t/*   {instr["result"]} = {instr["opcode"]} {instr["args"][0]}, {instr["args"][1]} [TAC] */')
        else:       # should have been caught before
            raise RuntimeError(f'Could not comment the instruction: {instr}')
    
    def __check_previous_instr(self, index: int, field: str, value_to_check: str) -> bool:
        """ Checks the previous instruction if a certain field in it has a certain value 

            Requirement: To check if we previous instruction is jmp to current label
                         To check if 
        """
        # print(self.__tac_instr[index])
        # print(self.__tac_instr[index][field], value_to_check)
        if field == 'args':   # compare the jmp argument with current label
          return self.__tac_instr[index][field][0] == value_to_check
        return self.__tac_instr[index][field] == value_to_check

    def __get_label_name(self, lab: str) -> str:
        """ appends the function name to the current label to mark a local label """
        return f'.{self.__func_name}{lab[1:]}'

    # ---------------------------------------------------------------------#
    # assertion functions
    # ---------------------------------------------------------------------#
        
    @staticmethod
    def __assert_temporary(temp: str, instr: dict) -> None:
        """ Checks if temporary is of correct format """
        assert (isinstance(temp, str) and \
                temp[0] == '%' and \
                temp[1:].isnumeric()), f'Invalid format for temporary in {instr}'

    @staticmethod
    def __assert_label(arg: str, instr: dict) -> None:
        """ Checks if label is of correct format """
        assert (isinstance(arg, str) and \
                arg.startswith('%.L') and \
                arg[3:].isnumeric()), f'Invalid format for label in {instr}'

    @staticmethod
    def __assert_argument_numb(args: List, num: int, instr: dict) -> None:
        """ Checks if correct number of arguments passed """
        if num == 1:
          assert (len(args)==1), f'Invalid number of arguments in {instr}'
        elif num == 2:
          assert (len(args)==2), f'Invalid number of arguments in {instr}'

    @staticmethod
    def __assert_result(result: None, instr: dict) -> None:
        """ Checks if result temporary is set to None """
        assert result == None, f'Result should be empty in {instr}'        

    # ---------------------------------------------------------------------#
    # tac to assembly conversion
    # ---------------------------------------------------------------------#

    def tac_to_asm(self):
        """ Get the x64 instructions corresponding to the TAC """

        for index, instr in enumerate(self.__tac_instr):
            
            assert isinstance(instr, dict), f'Invalid type for instruction: {instr}'
            # print(f"instr: {instr}")          # DEBUG

            self.__add_instr_comment(instr)     # Add coment in assembly file
            opcode = instr['opcode']
            args = instr['args']
            result = instr['result']

            if opcode == 'nop': pass

            elif opcode == 'label':
                self.__assert_argument_numb(args, 1, instr)
                arg = args[0]
                self.__assert_label(arg, instr)
                self.__assert_result(result, instr)
                
                # if previous instruction is jmp to current lab then comment the jmp
                if self.__check_previous_instr(index-1, 'opcode', 'jmp'): 
                    if self.__check_previous_instr(index-1, 'args', arg):
                        previos_instr_txt = self.__assembly[-2][1:]
                        self.__assembly[-2] = f'\t/* --{previos_instr_txt}-- */'
                self.__assembly.append(self.__get_label_name(arg)+':')          # add label to the assembly

            elif opcode == 'const':
                self.__assert_argument_numb(args, 1, instr)
                assert isinstance(args[0], int)                         # check if instruction is in correct format
                result = self.__lookup_temp(result, instr)        # get stack position to store result of temp
                self.__assembly.append(f'\tmovq ${args[0]}, {result}')    # add instruction as assembly

            elif opcode == 'copy':
                self.__assert_argument_numb(args, 1, instr)
                arg = self.__lookup_temp(args[0], instr)
                result = self.__lookup_temp(result, instr)
                self.__assembly.append(f'\tmovq {arg}, %r11')
                self.__assembly.append(f'\tmovq %r11, {result}')

            elif opcode in self.__binops:
                self.__assert_argument_numb(args, 2, instr)
                arg1 = self.__lookup_temp(args[0], instr)
                arg2 = self.__lookup_temp(args[1], instr)
                result = self.__lookup_temp(result, instr)
                bin_op = self.__binops[opcode]
                if isinstance(bin_op, str):
                    self.__assembly.extend([f'\tmovq {arg1}, %r11',
                                            f'\t{bin_op} {arg2}, %r11',
                                            f'\tmovq %r11, {result}'])
                else: 
                    self.__assembly.extend(bin_op(arg1, arg2, result))

            elif opcode in self.__unops:
                self.__assert_argument_numb(args, 1, instr)
                arg = self.__lookup_temp(args[0], instr)
                result = self.__lookup_temp(result, instr)
                un_op = self.__unops[opcode]
                self.__assembly.extend([f'\tmovq {arg}, %r11',
                                        f'\t{un_op} %r11',
                                        f'\tmovq %r11, {result}'])

            elif opcode == 'print':
                self.__assert_argument_numb(args, 1, instr)
                self.__assert_result(result, instr)
                arg = self.__lookup_temp(args[0], instr)
                # we are not using rax and rdi for simplicity
                # hence need not push them on the stack 
                self.__assembly.extend([f'\tmovq {arg}, %rdi',
                                        f'\tcallq bx_print_int'])

            elif opcode == 'jmp':
                self.__assert_argument_numb(args, 1, instr)
                self.__assert_result(result, instr)
                arg = args[0]
                self.__assembly.append(f'\tjmp {self.__get_label_name(arg)}')

            elif opcode in self.__jcc:
                self.__assert_argument_numb(args, 2, instr)
                arg = args[0]
                lab = args[1]
                self.__assert_temporary(arg, instr)
                self.__assert_label(lab, instr)
                self.__assert_result(result, instr)
                # if previous instruction is not a sub then we have a bool
                # condition and we need to test the argument value with 0 to
                # set the appropraite flags for the jcc instruction
                if not self.__check_previous_instr(index-1, 'opcode', 'sub'):
                    arg = self.__lookup_temp(arg, instr)
                    self.__assembly.append(f'\tcompq $0, {arg}')
                self.__assembly.append(f'\t{opcode} {self.__get_label_name(lab)}')

            else:       # where did we screw up?
                raise RuntimeError(f'Undefined opcode: {opcode}')


    def complete_assembly(self) -> List:
        """ Creates complete assembly code with stack manipulation of rbp and rsp """

        # convert the tac to assembly
        self.tac_to_asm()

        # set the stack size to the number of temporaries we need
        stack_size = len(self.__temp_map)
        if stack_size % 2 != 0: 
            stack_size += 1

        # Store the base pointer and initialize the stack pointer 
        self.__assembly[:0] = [f'\tpushq %rbp',
                               f'\tmovq %rsp, %rbp',
                               f'\tsubq ${8 * stack_size}, %rsp']

        # Reset the base pointer to the stack pointer
        self.__assembly.extend([f'\tmovq %rbp, %rsp',
                                f'\tpopq %rbp',
                                f'\tmovq $0, %rax',
                                f'\tretq'])

        return self.__assembly

# ------------------------------------------------------------------------------#
# main function drivers
# ------------------------------------------------------------------------------#

def compile_tac(fname: str) -> None:
    """ reads tac json file and converts it to x64 assembly """
    if fname.endswith('.tac.json'):
        read_name = fname[:-9]
    elif fname.endswith('.json'):
        read_name = fname[:-5]
    else:
        raise ValueError(f'{fname} is not of the correct format .tac.json or .json')

    with open(fname, 'rb') as fp:
        tac_jsn = json.load(fp)
    convert_instr_to_asm(read_name, tac_jsn)

def convert_instr_to_asm(fname: str, tac_jsn: list) -> None:
    """ Converts tac instructions list to assembly """
    # Check if fileformat is correct

    assert isinstance(tac_jsn, list) and len(tac_jsn) == 1, f'Invalid list structure of the input file\n {tac_jsn}'
    
    tac_jsn = tac_jsn[0]
    assert 'proc' in tac_jsn and tac_jsn['proc'] == '@main', f'Invalid function in {tac_jsn}'
    
    # Convert tac to assembly
    x64_asm = tac2x64(tac_jsn['proc'][1:], tac_jsn['body'])     # initialize tac2x64 class here 
    asm = x64_asm.complete_assembly()
    asm[:0] = [f'\t.text',
               f'\t.globl main',
               f'main:']
    
    # Save assembly code and create executable
    exe_name = fname + '.exe'
    asm_name = fname + '.s'
    with open(asm_name, 'w') as afp:
        print(*asm, file=afp, sep='\n')
    os.system(f'gcc -o {exe_name} {asm_name} bx_runtime.c')
    print(f"Compilation succesful for {fname}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} tacfile.tac.json')
        sys.exit(1)
    compile_tac(sys.argv[1])

