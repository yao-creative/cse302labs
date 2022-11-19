"""
    Module contains all Macros used in other modules in the compiler
"""

from typing import List, Any

# ---------------------------------------------------------------------#
# Macros used in bxast
# ---------------------------------------------------------------------#

class Operations:
    """ A class that declares all operations for global use """
    _binops_int: tuple = ("addition", "substraction", "multiplication",
                        "division", "modulus", "bitwise-and", "bitwise-or", 
                        "bitwise-xor", "logical-shift-left", "logical-shift-right")
    _binops_cmp: tuple = ("cmpl", "cmple", "cmpge", "cmpg", "cmpe", "cmpne")
    _binops_bool: tuple = ("logical-and", "logical-or")
    _binops: tuple = _binops_bool + _binops_cmp + _binops_int

    _unops_int: tuple = ("bitwise-negation", "opposite")
    _unops_bool: tuple = ("not",)
    _unops: tuple = _unops_bool + _unops_int

class BX_TYPE:
    """ Class of all the data types in BX """
    def getType(__name: str) -> Any:
        if __name == "int":
            return BX_TYPE.INT
        elif __name == "bool":
            return BX_TYPE.BOOL
        elif __name == "void":
            return BX_TYPE.VOID

    class INT: 
        """ Class of INT type """
        def __str__(self) -> str:
            return "int"

    class BOOL: 
        """ Class of BOOL type """
        def __str__(self) -> str:
            return "bool"
    
    class VOID:
        """ Class of VOID type """
        def __str__(self) -> str:
            return "void"

# ---------------------------------------------------------------------#
# Macros used in ast2tac
# ---------------------------------------------------------------------#

class tacMacros:
    """ The class contains mappings needed for parsing """

    operator_map = {
        "substraction": "sub", "addition": "add",
        "multiplication": "mul", "division": "div",
        "modulus": "mod", "bitwise-xor": "xor", 
        "bitwise-and": "and", "bitwise-or": "or",
        "logical-shift-right": "shr", "logical-shift-left": "shl",
        "opposite": "neg", "bitwise-negation": "not",
    }

    jump_map = {
        "cmpe": "jz", "cmpne": "jnz",
        "cmpl": "jl", "cmpg": "jnle",
        "cmple": "jle", "cmpge": "jnl",
    }

# ---------------------------------------------------------------------#
# Macros used in x64
# ---------------------------------------------------------------------#

class x64Macros:

    _binops={ 'add': 'addq',
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
                                          f'\tmovq %r11, {rd}'])
            }
    
    _unops = { 'neg': 'negq',
               'not': 'notq'}

    _jcc = ["je", "jz",       # Src2 == Src1
           "jne", "jnz",      # Src2 != Src1
           "jl", "jnge",      # Src2 < Src1
           "jle", "jng",      # Src2 <= Src1
           "jg", "jnle",      # Src2 > Src1
           "jge", "jnl",      # Src2 >= Src1
           ]

    _first_6_reg_moves = {  1 : (lambda temp: f'\tmovq {temp}, %rdi' ),
                            2 : (lambda temp: f'\tmovq {temp}, %rsi' ),
                            3 : (lambda temp: f'\tmovq {temp}, %rdx' ),
                            4 : (lambda temp: f'\tmovq {temp}, %rcx' ),
                            5 : (lambda temp: f'\tmovq {temp}, %r8' ),
                            6 : (lambda temp: f'\tmovq {temp}, %r9' ),
                        }

    _first_6_regs = { 0: "%rdi",
                      1: "%rsi",
                      2: "%rdx",
                      3: "%rcx",
                      4: "%r8",
                      5: "%r9"
                    }

    # ---------------------------------------------------------------------#
    # assertion functions
    # ---------------------------------------------------------------------#
        
    @staticmethod
    def _assert_temporary(temp: str, instr: dict) -> None:
        """ Checks if temporary is of correct format """
        assert (isinstance(temp, str)), f"Comparison can only happen with str in {instr}"
        if temp[0] == "@":
            assert (temp[1:].isalpha()), f'Global variable must be alpha in {instr}'
        else:
            assert (temp[0] == '%' and \
                    temp[1:].isnumeric()), f'Invalid format for temporary in {instr}'

    @staticmethod
    def _assert_label(arg: str, instr: dict) -> None:
        """ Checks if label is of correct format """
        assert (isinstance(arg, str) and \
                arg.startswith('%.L') and \
                arg[3:] == "entry" or arg[3:].isnumeric()), \
                f'Invalid format for label in {instr}'

    @staticmethod
    def _assert_argument_numb(args: List, num: int, instr: dict) -> None:
        """ Checks if correct number of arguments passed """
        if num == 1:
          assert (len(args)==1), f'Invalid number of arguments in {instr}'
        elif num == 2:
          assert (len(args)==2), f'Invalid number of arguments in {instr}'

    @staticmethod
    def _assert_result(result: None, instr: dict) -> None:
        """ Checks if result temporary is set to None """
        assert result == None, f'Result should be empty in {instr}'
