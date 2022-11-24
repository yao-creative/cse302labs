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
    def __init__(self, proc_args: list) -> None:
        self.__temp_map: Dict[str, str] = dict()
        self.__proc_args: List[str] = proc_args
        self.__proc_args_num: int = len(self.__proc_args)
        # self.__args_temp_init()

    def get_item(self, temp: str, instr: dict) -> str:
        """ Return the stack address of the temp """
        # if globl var then ret rip relative position
        # print(temp)
        if temp[0] == "@":
            return f'{temp[1:]}(%rip)'
        return self.__lookup_temp(temp, instr)

    def __lookup_temp(self, temp: str, instr: dict = None) -> str:
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

    def args_temp_init(self) -> List[str]:
        """ Initializes the temp map for all function arguments 
            and returns instructions for moving them to stack """
        param_instr = []
        for index in range(0, self.__proc_args_num):
            arg = self.__proc_args[index]
            if index < 6:
                temp = self.__lookup_temp(arg)
                param_instr.append(f"\tmovq {Macros._first_6_regs[index]}, {temp}")
                # self.__temp_map[arg] = f"{Macros._first_6_regs[index]}"
            else:
                offset = 8*(index - 4)
                assert(offset > 15), f' param {index} offset is invalid at {offset}(%rbp)'
                assert(offset <= (8*(self.__proc_args_num-5))), f' param {index} offset is invalid at {offset}(%rbp)'
                temp = self.__lookup_temp(arg)
                param_instr.append(f"\tmovq {offset}(%rbp), %r11")
                param_instr.append(f"\tmovq %r11, {temp}")
                # self.__temp_map[arg] = f"{offset}(%rbp)"
        return param_instr

    def start_proc(self, name: str) -> list:
        """ Adds initial commands when proc is entered """
        # set the stack size to the number of temporaries we need
        stack_size = len(self.__temp_map)
        stack_size += 1 if (stack_size % 2 != 0) else 0
        return [f'\n',
                f'\t.globl {name}',
                f'\t.text',
                f'{name}:',
                f'\tpushq %rbp',
                f'\tmovq %rsp, %rbp',
                f'\tsubq ${8*stack_size}, %rsp']

    def end_proc(self, proc_name: str) -> list:
        """ Adds final commands to end the proc """
        # Reset the base pointer to the stack pointer
        return [f'.{proc_name}.Lexit:',
                f'\tmovq %rbp, %rsp',
                f'\tpopq %rbp',
                f'\tretq\n']

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
        self.__asm_instr_gvar.append(f"\t.globl {self.__name}")
        self.__asm_instr_gvar.append(f"\t.data")
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
        self.__stack: Stack = Stack(self.__args)
        self.__create_asm_instr()

    # ---------------------------------------------------------------------#
    # misc functions
    # ---------------------------------------------------------------------#

    def __add_instr_comment(self, instr: dict) -> None:
        """ Adds instrs as a comment in the assembly """
        if instr['result'] == None:
            if instr['opcode'] == 'jmp' or instr['opcode'] == 'call':
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
        return f'.{self.__func_name}{lab[1:]}'      

    def __create_asm_instr(self) -> None:
        """ Runs other functions to create asm instr for the current proc """
        # convert the tac to assembly
        self.__tac_to_asm()
        # add initial instr when entering proc
        self.__asm_instr_proc[:0] = self.__stack.start_proc(self.__func_name)
        # add final instr when exiting proc
        self.__asm_instr_proc.extend(self.__stack.end_proc(self.__func_name))

    def return_asm_instr(self) -> List:
        """ Returns asm instrs for the current proc """
        return self.__asm_instr_proc

    # ---------------------------------------------------------------------#
    # tac to assembly conversion
    # ---------------------------------------------------------------------#

    def __tac_to_asm(self):
        """ Get the x64 instructions corresponding to the TAC """

        # initialize param instruction for the proc
        self.__asm_instr_proc = self.__stack.args_temp_init()        

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
                result = self.__stack.get_item(result, instr)        # get stack position to store result of temp
                self.__asm_instr_proc.append(f'\tmovq ${args[0]}, {result}')    # add instruction as assembly

            elif opcode == 'copy':
                # print(args, instr)
                Macros._assert_argument_numb(args, 1, instr)
                arg = self.__stack.get_item(args[0], instr)
                result = self.__stack.get_item(result, instr)
                self.__asm_instr_proc.append(f'\tmovq {arg}, %r11')
                self.__asm_instr_proc.append(f'\tmovq %r11, {result}')

            elif opcode in Macros._binops:
                Macros._assert_argument_numb(args, 2, instr)
                arg1 = self.__stack.get_item(args[0], instr)
                arg2 = self.__stack.get_item(args[1], instr)
                result = self.__stack.get_item(result, instr)
                bin_op = Macros._binops[opcode]
                if isinstance(bin_op, str):
                    self.__asm_instr_proc.extend([f'\tmovq {arg1}, %r11',
                                            f'\t{bin_op} {arg2}, %r11',
                                            f'\tmovq %r11, {result}'])
                else: 
                    self.__asm_instr_proc.extend(bin_op(arg1, arg2, result))

            elif opcode in Macros._unops:
                Macros._assert_argument_numb(args, 1, instr)
                arg = self.__stack.get_item(args[0], instr)
                result = self.__stack.get_item(result, instr)
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
                arg = self.__stack.get_item(arg, instr)
                self.__asm_instr_proc.append(f'\tcmpq $0, {arg}')
                self.__asm_instr_proc.append(f'\t{opcode} {self.__get_label_name(lab)}')

            elif opcode == "call":
                Macros._assert_argument_numb(args, 2, instr)
                assert(args[0][0]) == "@", f"Invalid call in the {instr}"
                arg_num = args[1]
                func = args[0]

                # if not 16 byte aligned then push 0 as last temp argument
                if arg_num > 6 and arg_num%2:
                    self.__asm_instr_proc.append(f'\tpushq $0')
                # push remaining params to stack in reverse order
                if arg_num > 6:
                    Macros._assert_argument_numb(self.__param_temps_for_call, arg_num-6, instr)
                    for param_temp in reversed(self.__param_temps_for_call):
                        self.__asm_instr_proc.append(f'\tpushq {self.__stack.get_item(param_temp, instr)}')

                self.__asm_instr_proc.append(f'\tcallq {func[1:]}')
                self.__param_temps_for_call = []        # reset param temps

                # add to stack pointer if more than 6 args
                if arg_num > 6:
                    self.__asm_instr_proc.append(f'\taddq ${8*(arg_num-6)}, %rsp')

                # if the call returns smth then transfer the result from rax
                if result is not None:
                    self.__asm_instr_proc.append(f'\tmovq %rax, {self.__stack.get_item(result, instr)}')


            elif opcode == "param":
                Macros._assert_argument_numb(args, 2, instr)
                arg_temp = args[1]
                arg_num = args[0]
                if arg_num <= 6:
                    self.__asm_instr_proc.append(Macros._first_6_reg_moves[arg_num](self.__stack.get_item(arg_temp, instr)))
                # add remaining params in reverse order to list that will be pushed before callq
                if arg_num > 6:
                    assert(arg_temp not in self.__param_temps_for_call)
                    self.__param_temps_for_call.append(arg_temp)

            elif opcode == "ret":
                if len(args) == 0:
                    self.__asm_instr_proc.append(f'\txorq %rax, %rax')
                else:
                    Macros._assert_argument_numb(args, 1, instr)
                    arg = self.__stack.get_item(args[0], instr)
                    self.__asm_instr_proc.append(f'\tmovq {arg}, %rax')
                # We jmp to the last exit label of the proc 
                self.__asm_instr_proc.append(f'\tjmp .{self.__func_name}.Lexit')

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
        self.__asm_alloc()

    def __parse_tac(self) -> None:
        """ Get asm instr for all tac members """
        for member in self.__tac_list:
            if "var" in member:
                self.__globl_vars_list.append(GlobalVarx64(member))
            elif "proc" in member:
                self.__proc_list.append(Procx64(member))
            else:
                raise RuntimeError(f"Unexpected Tac type {member}")

    def __asm_alloc(self) -> None:
        """ Allocates appropraite instrs for all globl decls """
        for var in self.__globl_vars_list:
            self.__x64_list.append(var.get_instr())
        for proc in self.__proc_list:
            self.__x64_list.append(proc.return_asm_instr())

    def get_asm_instr(self) -> list:
        """ returns the asm instrs for the entire code """
        return self.__x64_list

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
    asm = x64_asm.get_asm_instr()

    # Save assembly code and create executable
    exe_name = fname + '.exe'
    asm_name = fname + '.s'
    with open(asm_name, 'w') as afp:
        total = []
        for globl in asm:
            total+=globl
        tac_ = "\n".join(total)
        afp.write(tac_)
        # print(*asm, file=afp, sep='\n')
    os.system(f'gcc -o {exe_name} {asm_name} bx_runtime.c')
    print(f"Compilation succesful for {fname}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} tacfile.tac.json')
        sys.exit(1)
    compile_tac(sys.argv[1])

