import json, sys, os
from pathlib import Path
from typing import List
"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

class tac2x64:

    def __init__(self, functn: str, tac_instrs: List) -> None:
        self.tac_instr: List = tac_instrs
        self.func_name: str = functn
        self.assembly: List = []
        self.temp_map: dict = {}

    # ---------------------------------------------------------------------#
    # Class Macro Variables
    # ---------------------------------------------------------------------#

    binops = {'add': 'addq',
              'sub': 'subq',
              'mul': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                          f'imulq {rb}',
                                          f'movq %rax, {rd}']),
              'div': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                          f'cqto',
                                          f'idivq {rb}',
                                          f'movq %rax, {rd}']),
              'mod': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                          f'cqto',
                                          f'idivq {rb}',
                                          f'movq %rdx, {rd}']),
              'and': 'andq',
              'or': 'orq',
              'xor': 'xorq',
              'shl': (lambda ra, rb, rd: [f'movq {ra}, %r11',
                                          f'movq {rb}, %rcx',
                                          f'salq %cl, %r11',
                                          f'movq %r11, {rd}']),
              'shr': (lambda ra, rb, rd: [f'movq {ra}, %r11',
                                          f'movq {rb}, %rcx',
                                          f'sarq %cl, %r11',
                                          f'movq %r11, {rd}'])}
    unops = {'neg': 'negq',
            'not': 'notq'}

    jcc = ["je", "jz"         # Src2 == Src1
           "jne", "jnz",      # Src2 != Src1
           "jl", "jnge",      # Src2 < Src1
           "jle", "jng",      # Src2 <= Src1
           "jg", "jnle",      # Src2 > Src1
           "jge", "jnl",      # Src2 >= Src1
           ]

    # ---------------------------------------------------------------------#
    # misc functions
    # ---------------------------------------------------------------------#

    def lookup_temp(self, temp: str, instr: dict) -> str:
        """ Returns the value of the temp from the stack 
            while simultaneously creating a hash table """
        self.check_temporary(temp, instr)
        return self.temp_map.setdefault(temp, f'{-8 * (len(self.temp_map) + 1)}(%rbp)')

    def add_instr_comment(self, instr: dict) -> None:
        """ Adds instruction as a comment in the assembly """

        if instr['result'] == None:
            if instr['opcode'] == 'jmp' or instr['opcode'] == 'print':
                self.assembly.append(f'\t/*   {instr["opcode"]} {instr["args"][0]} [TAC] */')
            elif instr['opcode'] in self.jcc:
                self.assembly.append(f'\t/*   {instr["opcode"]} {instr["args"][0]}, {instr["args"][1]} [TAC] */')
            elif instr['opcode'] == 'label':
                self.assembly.append(f'\t/*  {instr["args"][0]}: [TAC] */')
        
        elif len(instr["args"]) == 1:
            self.assembly.append(f'\t/*   {instr["result"]} = {instr["opcode"]} {instr["args"][0]} [TAC] */')
        
        elif len(instr["args"]) == 2:
            self.assembly.append(f'\t/*   {instr["result"]} = {instr["opcode"]}, {instr["args"][0]}, {instr["args"][1]} [TAC] */')
        
        else:       # should have been caught before
            raise RuntimeError(f'Could not comment the instruction: {instr}')
    
    def check_prv_instr(self, index: int, field: str, value_to_check: str) -> bool:
        """ Checks the previous instruction if it has a certain value """
        # print(self.tac_instr[index])
        # print(self.tac_instr[index][field], value_to_check)
        if field == 'args':   # compare the jmp argument with current label
          return self.tac_instr[index][field][0] == value_to_check
        return self.tac_instr[index][field] == value_to_check

    def get_label_name(self, lab: str) -> str:
        """ returns a label name for the current function """
        return f'.{self.func_name}{lab[1:]}'

    # ---------------------------------------------------------------------#
    # assertion functions
    # ---------------------------------------------------------------------#
        
    @staticmethod
    def check_temporary(temp: str, instr: dict) -> None:
        """ Checks if temporary is of correct format """
        assert (isinstance(temp, str) and \
                temp[0] == '%' and \
                temp[1:].isnumeric()), f'Invalid format for temporary in {instr}'

    @staticmethod
    def check_label(arg: str, instr: dict) -> None:
        """ Checks if label is of correct format """
        assert (isinstance(arg, str) and \
                arg.startswith('%.L') and \
                arg[3:].isnumeric()), f'Invalid format for label in {instr}'

    @staticmethod
    def check_arguments(args: List, num: int, instr: dict) -> None:
        """ Checks if correct number of arguments passed """
        if num == 1:
          assert (len(args)==1), f'Invalid number of arguments in {instr}'
        elif num == 2:
          assert (len(args)==2), f'Invalid number of arguments in {instr}'

    @staticmethod
    def check_result(result: None, instr: dict) -> None:
        """ Checks if result temporary is set to None """
        assert result == None, f'Result should be empty in {instr}'        

    # ---------------------------------------------------------------------#
    # tac to assembly conversion
    # ---------------------------------------------------------------------#

    def tac_to_asm(self):
        """ Get the x64 instructions corresponding to the TAC """

        for index, instr in enumerate(self.tac_instr):
            
            assert isinstance(instr, dict), f'Invalid type for instruction: {instr}'
            # print(f"instr: {instr}")          # DEBUG

            self.add_instr_comment(instr)     # Add coment in assembly file
            opcode = instr['opcode']
            args = instr['args']
            result = instr['result']

            if opcode == 'nop': pass

            elif opcode == 'label':
                self.check_arguments(args, 1, instr)
                arg = args[0]
                self.check_label(arg, instr)
                self.check_result(result, instr)
                
                # if previous instruction is jmp to current lab then comment the jmp
                if self.check_prv_instr(index-1, 'opcode', 'jmp'): 
                    if self.check_prv_instr(index-1, 'args', arg):
                        # TODO
                        pass
                self.assembly.append(self.get_label_name(arg)+':')          # add label to the assembly

            elif opcode == 'const':
                self.check_arguments(args, 1, instr)
                assert isinstance(args[0], int)                         # check if instruction is in correct format
                result = self.lookup_temp(result, instr)        # get stack position to store result of temp
                self.assembly.append(f'\tmovq ${args[0]}, {result}')    # add instruction as assembly

            elif opcode == 'copy':
                self.check_arguments(args, 1, instr)
                arg = self.lookup_temp(args[0], instr)
                result = self.lookup_temp(result, instr)
                self.assembly.append(f'\tmovq {arg}, %r11')
                self.assembly.append(f'\tmovq %r11, {result}')

            elif opcode in self.binops:
                self.check_arguments(args, 2, instr)
                arg1 = self.lookup_temp(args[0], instr)
                arg2 = self.lookup_temp(args[1], instr)
                result = self.lookup_temp(result, instr)
                bin_op = self.binops[opcode]
                if isinstance(bin_op, str):
                    self.assembly.extend([f'\tmovq {arg1}, %r11',
                                          f'\t{bin_op} {arg2}, %r11',
                                          f'\tmovq %r11, {result}'])
                else: 
                    self.assembly.extend(bin_op(arg1, arg2, result))

            elif opcode in self.unops:
                self.check_arguments(args, 1, instr)
                arg = self.lookup_temp(args[0], instr)
                result = self.lookup_temp(result, instr)
                un_op = self.unops[opcode]
                self.assembly.extend([f'\tmovq {arg}, %r11',
                                      f'\t{un_op} %r11',
                                      f'\tmovq %r11, {result}'])

            elif opcode == 'print':
                self.check_arguments(args, 1, instr)
                self.check_result(result, instr)
                arg = self.lookup_temp(args[0], instr)
                self.assembly.extend([f'\tmovq {arg}, %rdi',
                                      f'\tcallq bx_print_int'])

            elif opcode == 'jmp':
                self.check_arguments(args, 1, instr)
                self.check_result(result, instr)
                arg = args[0]
                self.assembly.append(f'\tjmp {self.get_label_name(arg)}')

            elif opcode in self.jcc:
                self.check_arguments(args, 2, instr)
                arg = args[0]
                lab = args[1]
                self.check_temporary(arg, instr)
                self.check_label(lab, instr)
                self.check_result(result, instr)
                # if previous instruction is not a sub then we need to compare
                if not self.check_prv_instr(index-1, 'opcode', 'sub'):
                    arg = self.lookup_temp(arg, instr)
                    self.assembly.extend([f'\tmovq {arg}, %r11',
                                          f'\ttestq %r11, %r11'])
                self.assembly.append(f'\t{opcode} {self.get_label_name(lab)}')

            else:       # where did we screw up?
                raise RuntimeError(f'Undefined opcode: {opcode}')


    def complete_assembly(self) -> List:
        """ Creates complete assembly code with stack manipulation """

        # convert the tac to assembly
        self.tac_to_asm()

        # set the stack size to the number of temporaries we need
        stack_size = len(self.temp_map)
        if stack_size % 2 != 0: 
            stack_size += 1         # 16 byte alignment for x64

        # Store the base pointer and initialize the stack pointer 
        self.assembly[:0] = [f'\tpushq %rbp',
                             f'\tmovq %rsp, %rbp',
                             f'\tsubq ${8 * stack_size}, %rsp']

        # Reset the base pointer to the stack pointer
        self.assembly.extend([f'\tmovq %rbp, %rsp',
                              f'\tpopq %rbp',
                              f'\tmovq $0, %rax',
                              f'\tretq'])

        return self.assembly

# ------------------------------------------------------------------------------#
# main function drivers
# ------------------------------------------------------------------------------#

def compile_tac(fname):

    # Check if fileformat is correct
    if fname.endswith('.tac.json'):
        rname = fname[:-9]
    elif fname.endswith('.json'):
        rname = fname[:-5]
    else:
        raise ValueError(f'{fname} is not of the correct format .tac.json or .json')
    
    # Open file and check if it has correct structure
    tac_jsn = None
    with open(fname, 'rb') as fp:
        tac_jsn = json.load(fp)
    assert isinstance(tac_jsn, list) and len(tac_jsn) == 1, tac_jsn
    tac_jsn = tac_jsn[0]
    assert 'proc' in tac_jsn and tac_jsn['proc'] == '@main', tac_jsn
    
    # Convert tac to assembly
    x64_asm = tac2x64(tac_jsn['proc'][1:], tac_jsn['body'])     # initialize tac2x64 class here 
    asm = x64_asm.complete_assembly()
    asm[:0] = [f'\t.text',
               f'\t.globl main',
               f'main:']
    
    # Save assembly code and create executable
    xname = rname + '.exe'
    sname = rname + '.s'
    with open(sname, 'w') as afp:
        print(*asm, file=afp, sep='\n')
    os.system(f'gcc -o {xname} {sname} bx_runtime.c')
    print(f'{fname} -> {sname}')
    print(f'{sname} -> {xname}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} tacfile.tac.json')
        sys.exit(1)
    compile_tac(sys.argv[1])
