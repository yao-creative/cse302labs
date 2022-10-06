import sys
import json
from typing import Union
from bxast import *

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

# ------------------------------------------------------------------------------#
# Helper Classes
# ------------------------------------------------------------------------------#

class Code_Macro:
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


class Code_State:
    """ The class keeps track of helper information 
        needed to track TAC stmt generation """

    def __init__(self, func: str) -> None:
        self.func_name: str = func
        self.temps: dict = {}
        self.labels: list = []  
        self.__break_stack = []
        self.__continue_stack = []
    
    
class TAC_line:
    """ This class generates single tac line for each instruction """
    def __init__(self, opcode: str, args: List, result: str):
        self.opcode: str = opcode
        self.args: List = args
        self.result: str = result
    
    def format(self) -> Dict[str, Union[str, List[str]]]:
        """ Returns tac instruction as a json object """
        return {"opcode": self.opcode, 
                "args": self.args, 
                "result": self.result }

# ------------------------------------------------------------------------------#
# Typed Maximul Munch Class
# ------------------------------------------------------------------------------#

class AST_to_TAC_Generator:
    """ Takes the AST tree and converts it to TAC """
    def __init__(self, tree: DeclProc):
        self.code_state: Code_State = Code_State("main")
        self.code: DeclProc = tree
        self.instructions: List[TAC_line] = []
        self.begin_parse(self.code.body)

    def tac_generator(self) -> json:
        """ Generates the tac file """
        return {"proc": '@'+self.code.name,
                "body": [instr.format() for instr in self.instructions],
                "temps": self.code_state.temps,
                "labels": self.code_state.labels}

    def statement_parse(self, statement) -> None:
        """ parses the statement and builds its tac """
        if isinstance(statement, StatementBlock):
            pass

        elif isinstance(statement, StatementWhile):
            pass
        
        elif isinstance(statement, StatementIfElse):
            pass

        elif isinstance(statement, StatementJump):
            pass

        elif isinstance(statement, StatementVardecl):
            pass

        elif isinstance(statement, StatementAssign):
            pass

        elif isinstance(statement, StatementPrint):
            pass

    def int_expression_parse(self, expression: Expression) -> None:
        """ parses the expression and builds its tac """
        if expression.type != INT:
            raise RuntimeError(f'Expression must have type INT but has type {expression.type}')
        
        if isinstance(expression, ExpressionInt):
            pass

        elif isinstance(expression, ExpressionVar):
            pass

        elif isinstance(expression, ExpressionOp):
            pass

    def bool_expression_parse(self, expression: Expression) -> None:
        """ parses the expression and builds its tac """
        if expression.type != BOOL:
            raise RuntimeError(f'Expression must have type BOOL but has type {expression.type}')
        
        if isinstance(expression, ExpressionBool):
            pass

        elif isinstance(expression, ExpressionOp):
            pass


# ------------------------------------------------------------------------------#
# Main function
# ------------------------------------------------------------------------------#

import argparse
import my_parser as lexer_parser

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Get method for conversion and filetype.')
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename

    with open(filename, 'r') as fp:             # read the bx code as text
        code = fp.read()

    ast_: DeclProc = lexer_parser.run_parser(code)        # run lexer and parser
    if ast_ is None: 
        raise SyntaxError("Could not compile ast")          # exit if error occured while parsing 
    ast_.type_check()                         # check syntax
    print('reached tac json')
    tac_code = AST_to_TAC_Generator(ast_)   # convert ast code to json
    print("tac json created")
    tac_filename = filename[:-2] + 'tac.json'   # get new file name
    with open(tac_filename, 'w') as fp:         # save the file
        # json.dump(tac_code.json_tac(), fp, indent=4)
        pass
