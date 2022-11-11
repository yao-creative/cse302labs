import json, sys, os
from typing import List
from macros import x64Macros as Macros

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

# ---------------------------------------------------------------------#
# Class for Global Vars
# ---------------------------------------------------------------------#

class GlobalVarx64:
    def __init__(self, var: dict) -> None:
        self.__name: str = var["var"][1:]
        self.__init: str = var["init"]
        self.__asm_instr: list = list()
        self.__create_asm()

    def __create_asm(self) -> None:
        """ Creates x64 asm instr from the given tac instr """
        self.__asm_instr.append(f"\tglobl {self.__name}")
        self.__asm_instr.append(f"\tdata")
        self.__asm_instr.append(f"{self.__name}:  .quad {self.__init}")

    def get_instr(self) -> list:
        """ Returns the assembly instructions of the global variables """
        return self.__asm_instr

# ---------------------------------------------------------------------#
# Class for Procs
# ---------------------------------------------------------------------#

class Procx64:
    def __init__(self, proc_instrs: List) -> None:
        self.__func_name: str = proc_instrs["proc"][1:]
        self.__args: list = proc_instrs["args"]
        self.__tac_instr: list = proc_instrs["body"]
        self.__temps: list = proc_instrs["temps"]
        self.__labels: list = proc_instrs["labels"]
        self.__assembly: List = list()
        self.__temp_map: dict = dict()

    # ---------------------------------------------------------------------#
    # misc functions
    # ---------------------------------------------------------------------#

    def __lookup_temp(self, temp: str, instr: dict) -> str:
        """ Returns the value of the temp from the stack 
            while simultaneously creating a hash table """
        Macros._assert_temporary(temp, instr)
        # if temporary already exists return its value
        if temp in self.__temp_map:
            return self.__temp_map[temp]
        # add a new destination for it considering there is one address for rsp
        else:
            self.__temp_map[temp] = f'{-8 * (len(self.__temp_map) + 1)}(%rbp)'
        return self.__temp_map[temp]

    def __add_instr_comment(self, instr: dict) -> None:
        """ Adds instruction as a comment in the assembly """
        if instr['result'] == None:
            if instr['opcode'] == 'jmp' or instr['opcode'] == 'print':
                self.__assembly.append(f'\t/*   {instr["opcode"]} {instr["args"][0]} [TAC] */')
            elif instr['opcode'] in Macros._jcc:
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
        return f'%{lab[1:]}'      

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
                Macros._assert_argument_numb(args, 1, instr)
                arg = args[0]
                Macros._assert_label(arg, instr)
                Macros._assert_result(result, instr)
                
                # if previous instruction is jmp to current lab then comment the jmp
                if self.__check_previous_instr(index-1, 'opcode', 'jmp'): 
                    if self.__check_previous_instr(index-1, 'args', arg):
                        previos_instr_txt = self.__assembly[-2][1:]
                        self.__assembly[-2] = f'\t/* --{previos_instr_txt}-- */'
                self.__assembly.append(self.__get_label_name(arg)+':')          # add label to the assembly

            elif opcode == 'const':
                Macros._assert_argument_numb(args, 1, instr)
                assert isinstance(args[0], int)                         # check if instruction is in correct format
                result = self.__lookup_temp(result, instr)        # get stack position to store result of temp
                self.__assembly.append(f'\tmovq ${args[0]}, {result}')    # add instruction as assembly

            elif opcode == 'copy':
                Macros._assert_argument_numb(args, 1, instr)
                arg = self.__lookup_temp(args[0], instr)
                result = self.__lookup_temp(result, instr)
                self.__assembly.append(f'\tmovq {arg}, %r11')
                self.__assembly.append(f'\tmovq %r11, {result}')

            elif opcode in Macros._binops:
                Macros._assert_argument_numb(args, 2, instr)
                arg1 = self.__lookup_temp(args[0], instr)
                arg2 = self.__lookup_temp(args[1], instr)
                result = self.__lookup_temp(result, instr)
                bin_op = Macros._binops[opcode]
                if isinstance(bin_op, str):
                    self.__assembly.extend([f'\tmovq {arg1}, %r11',
                                            f'\t{bin_op} {arg2}, %r11',
                                            f'\tmovq %r11, {result}'])
                else: 
                    self.__assembly.extend(bin_op(arg1, arg2, result))

            elif opcode in Macros._unops:
                Macros._assert_argument_numb(args, 1, instr)
                arg = self.__lookup_temp(args[0], instr)
                result = self.__lookup_temp(result, instr)
                un_op = Macros._unops[opcode]
                self.__assembly.extend([f'\tmovq {arg}, %r11',
                                        f'\t{un_op} %r11',
                                        f'\tmovq %r11, {result}'])

            elif opcode == 'print':
                Macros._assert_argument_numb(args, 1, instr)
                Macros._assert_result(result, instr)
                arg = self.__lookup_temp(args[0], instr)
                # we are not using rax and rdi for simplicity
                # hence need not push them on the stack 
                self.__assembly.extend([f'\tmovq {arg}, %rdi',
                                        f'\tcallq bx_print_int'])

            elif opcode == 'jmp':
                Macros._assert_argument_numb(args, 1, instr)
                Macros._assert_result(result, instr)
                arg = args[0]
                self.__assembly.append(f'\tjmp {self.__get_label_name(arg)}')

            elif opcode in Macros._jcc:
                Macros._assert_argument_numb(args, 2, instr)
                arg = args[0]
                lab = args[1]
                Macros._assert_temporary(arg, instr)
                Macros._assert_label(lab, instr)
                Macros._assert_result(result, instr)
                # if previous instruction is not a sub then we have a bool
                # condition and we need to test the argument value with 0 to
                # set the appropraite flags for the jcc instruction
                if not self.__check_previous_instr(index-1, 'opcode', 'sub'):
                    arg = self.__lookup_temp(arg, instr)
                    self.__assembly.append(f'\tcmpq $0, {arg}')
                self.__assembly.append(f'\t{opcode} {self.__get_label_name(lab)}')

            elif opcode == "call":
                Macros._assert_argument_numb(args, 2, instr)
                assert(args[0][0]) == "@", f"Invalid call in the {instr}"

            elif opcode == "param":
                Macros._assert_argument_numb(args, 2, instr)

            elif opcode == "ret":
                if args == []:
                    self.__assembly.append(f'')
                else:
                    Macros._assert_argument_numb(args, 1, instr)

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
# Main x64 class
# ------------------------------------------------------------------------------#

class tac2x64:
    def __init__(self, tac: list) -> None:
        self.__tac_list: List[dict] = tac
        self.__globl_vars_list: List[GlobalVarx64] = list()
        self.__proc_list: List[Procx64] = list()
        self.__x64_list: List[list] = list()
        self.__parse_tac()

    def __parse_tac(self) -> None:
        """ Get asm instr for all tac members """
        for member in self.__tac_list:
            if "var" in member:
                self.__globl_vars_list.append(GlobalVarx64(member))
            elif "proc" in member:
                self.__proc_list.append(Procx64(member))
            else:
                raise RuntimeError(f"Unexpected Tac type {member}")

    def __stack_alloc(self) -> None:
        """ Allocates appropraite memory for all procs """

# ------------------------------------------------------------------------------#
# Main function drivers
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

    assert isinstance(tac_jsn, list), f'Tac instr should be a list\n'

    # Convert tac to assembly
    x64_asm = tac2x64(tac_jsn)     # initialize tac2x64 class here 
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

