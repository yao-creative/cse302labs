import json, sys, os
from typing import List, Dict
from macros import x64Macros as Macros

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

# ---------------------------------------------------------------------#
# Class to handle Stack
# ---------------------------------------------------------------------#

class Stack:
    def __init__(self) -> None:
        self.__temp_map: Dict[str, str] = dict()
        self.__stack_size: int

    def __getitem__(self, temp: str, instr: dict) -> str:
        """ Return the stack address of the temp """
        # if globl var then ret rip relative position
        if temp[0] == "@":
            return f'{temp[1:]}(%rip)'
        return self.__temp_map(temp, instr)

    def __lookup_temp(self, temp: str, instr: dict) -> str:
        """ Returns the value of the temp from the stack 
            while simultaneously creating a hash table """
        Macros._assert_temporary(temp, instr)
        # if temporary already exists return its value
        if temp in self.__temp_map:
            return self.__temp_map[temp]
        # add a new destination for it considering there is one address for rsp
        else:
            self.__temp_map[temp] = f'{-8 * (len(self.__temp_map)+1)}(%rbp)'
        return self.__temp_map[temp]

    def temp_init(self, tac_args: dict) -> None:
        """ Initializes the temp map for all args """

        # TODO don't need to alloc stack space for params

        for index in range(len(tac_args)):
            arg = tac_args[index]
            if index < 6:
                stack_loc = f"{-8 * (len(self.__temp_map)+1)}(%rbp)"
                self.__temp_map[arg] = stack_loc
            else:
                offset = 8*(index - 5)
                assert()

        # TODO alloc stack space for all other temps

        self.__stack_size = len(self.__temp_map)

    def start_proc(self, name: str) -> list:
        """ Adds initial commands when proc is entered """
        # set the stack size to the number of temporaries we need
        stack_size = self.__stack_size
        stack_size += 1 if (stack_size % 2 != 0) else 0
        return [f'\n',
                f'\t.globl {name}',
                f'\t.text',
                f'{name}:',
                f'\tpushq %rbp',
                f'\tmovq %rsp, %rbp',
                f'\tsubq ${stack_size}, %rsp']

    def end_proc(self) -> list:
        """ Adds final commands to end the proc """
        # Reset the base pointer to the stack pointer
        return [f'.Lexit'
                f'\tmovq %rbp, %rsp',
                f'\tpopq %rbp',
                f'\tretq']

# ---------------------------------------------------------------------#
# Class for Global Vars
# ---------------------------------------------------------------------#

class GlobalVarx64:
    def __init__(self, var: dict) -> None:
        self.__name: str = var["var"][1:]
        self.__init: str = var["init"]
        self.__asm_instr_gvar: list = list()
        self.__create_asm()

    def __create_asm(self) -> None:
        """ Creates x64 asm instr from the given tac instr """
        self.__asm_instr_gvar.append(f"\tglobl {self.__name}")
        self.__asm_instr_gvar.append(f"\tdata")
        self.__asm_instr_gvar.append(f"{self.__name}:  .quad {self.__init}")

    def get_instr(self) -> list:
        """ Returns the assembly instructions of the global variables """
        return self.__asm_instr_gvar

# ---------------------------------------------------------------------#
# Class for Procs
# ---------------------------------------------------------------------#

class Procx64():
    def __init__(self, proc_instrs: List) -> None:
        self.__func_name: str = proc_instrs["proc"][1:]
        self.__args: list = proc_instrs["args"]
        self.__param_temps_for_call: list = list()
        self.__tac_instr: list = proc_instrs["body"]
        self.__temps: list = proc_instrs["temps"]
        self.__labels: list = proc_instrs["labels"]
        self.__asm_instr_proc: List = list()
        self.__stack: Stack = Stack()

    # ---------------------------------------------------------------------#
    # misc functions
    # ---------------------------------------------------------------------#

    def __add_instr_comment(self, instr: dict) -> None:
        """ Adds instruction as a comment in the assembly """
        if instr['result'] == None:
            if instr['opcode'] == 'jmp' or instr['opcode'] == 'print':
                self.__asm_instr_proc.append(f'\t/*   {instr["opcode"]} {instr["args"][0]} [TAC] */')
            elif instr['opcode'] in Macros._jcc:
                self.__asm_instr_proc.append(f'\t/*   {instr["opcode"]} {instr["args"][0]}, {instr["args"][1]} [TAC] */')
            elif instr['opcode'] == 'label':
                self.__asm_instr_proc.append(f'\t/*  {instr["args"][0]}: [TAC] */')
        elif len(instr["args"]) == 1:
            self.__asm_instr_proc.append(f'\t/*   {instr["result"]} = {instr["opcode"]} {instr["args"][0]} [TAC] */')
        elif len(instr["args"]) == 2:
            self.__asm_instr_proc.append(f'\t/*   {instr["result"]} = {instr["opcode"]} {instr["args"][0]}, {instr["args"][1]} [TAC] */')
        else:       # should have been caught before
            raise RuntimeError(f'Could not comment the instruction: {instr}')

    def __check_previous_instr(self, index: int, field: str, value_to_check: str) -> bool:
        """ Checks the previous instruction if a certain field in it has a certain value 
            Requirement: To check if previous instr is jmp to current label
                         To check if previous instr is a sub
        """
        # print(self.__tac_instr[index])
        # print(self.__tac_instr[index][field], value_to_check)
        if field == 'args':   # compare the jmp argument with current label
            return self.__tac_instr[index][field][0] == value_to_check
        return self.__tac_instr[index][field] == value_to_check

    def __get_label_name(self, lab: str) -> str:
        """ appends the function name to the current label to mark a local label """
        return f'.{self.__func_name}.{lab[1:]}'      

    def __temp_for_param(self) -> str:
        """ Creates a new temp for param instr """
        new_temp = f"%{len(self.__temps)}"
        self.__temps.append(new_temp)
        self.__param_temps_for_call.append(new_temp)
        return new_temp

    def __create_asm_instr(self) -> None:
        """ Runs other functions to create asm instr """
        # add initial instr when entering proc
        self.__asm_instr_proc = self.__stack.start_proc(self.__func_name)
        # convert the tac to assembly
        self.__tac_to_asm()
        # add final instr when exiting proc
        self.__asm_instr_proc.extend(self.__stack.end_proc())

    def return_asm_instr(self) -> List:
        """ Returns the complete assembly code """
        self.__create_asm_instr()
        return self.__asm_instr_proc

    # ---------------------------------------------------------------------#
    # tac to assembly conversion
    # ---------------------------------------------------------------------#

    def __tac_to_asm(self):
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
                        previos_instr_txt = self.__asm_instr_proc[-2][1:]
                        self.__asm_instr_proc[-2] = f'\t/* --{previos_instr_txt}-- */'
                self.__asm_instr_proc.append(self.__get_label_name(arg)+':')          # add label to the assembly

            elif opcode == 'const':
                Macros._assert_argument_numb(args, 1, instr)
                assert isinstance(args[0], int)                         # check if instruction is in correct format
                result = self.__stack[result, instr]        # get stack position to store result of temp
                self.__asm_instr_proc.append(f'\tmovq ${args[0]}, {result}')    # add instruction as assembly

            elif opcode == 'copy':
                Macros._assert_argument_numb(args, 1, instr)
                arg = self.__stack[args[0], instr]
                result = self.__stack[result, instr]
                self.__asm_instr_proc.append(f'\tmovq {arg}, %r11')
                self.__asm_instr_proc.append(f'\tmovq %r11, {result}')

            elif opcode in Macros._binops:
                Macros._assert_argument_numb(args, 2, instr)
                arg1 = self.__stack[args[0], instr]
                arg2 = self.__stack[args[1], instr]
                result = self.__stack[result, instr]
                bin_op = Macros._binops[opcode]
                if isinstance(bin_op, str):
                    self.__asm_instr_proc.extend([f'\tmovq {arg1}, %r11',
                                            f'\t{bin_op} {arg2}, %r11',
                                            f'\tmovq %r11, {result}'])
                else: 
                    self.__asm_instr_proc.extend(bin_op(arg1, arg2, result))

            elif opcode in Macros._unops:
                Macros._assert_argument_numb(args, 1, instr)
                arg = self.__stack[args[0], instr]
                result = self.__stack[result, instr]
                un_op = Macros._unops[opcode]
                self.__asm_instr_proc.extend([f'\tmovq {arg}, %r11',
                                        f'\t{un_op} %r11',
                                        f'\tmovq %r11, {result}'])

            elif opcode == 'jmp':
                Macros._assert_argument_numb(args, 1, instr)
                Macros._assert_result(result, instr)
                arg = args[0]
                self.__asm_instr_proc.append(f'\tjmp {self.__get_label_name(arg)}')

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
                    arg = self.__stack[arg, instr]
                    self.__asm_instr_proc.append(f'\tcmpq $0, {arg}')
                self.__asm_instr_proc.append(f'\t{opcode} {self.__get_label_name(lab)}')

            # TODO check if this is right
            elif opcode == "call":
                Macros._assert_argument_numb(args, 2, instr)
                assert(args[0][0]) == "@", f"Invalid call in the {instr}"
                arg_num = args[1]
                func = args[0]
                # add first 6 params to regs
                for i in range(min(arg_num, 6)):
                    temp = self.__param_temps_for_call[index]
                    self.__asm_instr_proc.append(Macros._first_6_regs[i](temp))
                # add remaining params in reverse order to stack
                if arg_num > 6:
                    for temp in reversed(self.__param_temps_for_call[6:]):
                        self.__asm_instr_proc.append(f'\tpushq {temp}')
                self.__asm_instr_proc.append(f'\tcallq {func[1:]}')

            # TODO check if this is right
            elif opcode == "param":
                Macros._assert_argument_numb(args, 2, instr)
                arg_temp = args[1]
                # copy temp to a new temp
                new_temp = self.__temp_for_param()
                self.__asm_instr_proc.append(f'\tmovq {arg_temp}, %r11')
                self.__asm_instr_proc.append(f'\tmovq %r11, {new_temp}')

            elif opcode == "ret":
                if len(args) == 0:
                    self.__asm_instr_proc.append(f'\txorq %rax, %rax')
                else:
                    Macros._assert_argument_numb(args, 1, instr)
                    arg = self.__stack[args[0], instr]
                    self.__asm_instr_proc.append(f'\tmovq {arg}, %rax')
                self.__asm_instr_proc.append(f'\tretq')

            else:       # where did we screw up?
                raise RuntimeError(f'Undefined opcode: {opcode}')

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

