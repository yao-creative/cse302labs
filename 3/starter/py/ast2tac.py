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

class TAC_line:
    """ This class generates single tac line for each instruction """
    def __init__(self, opcode: str, args: List, result: str):
        self.__opcode: str = opcode
        self.__args: List = args
        self.__result: str = result
    
    def format(self) -> Dict[str, Union[str, List[str]]]:
        """ Returns tac instruction as a json object """
        return {"opcode": self.__opcode, 
                "args": self.__args, 
                "result": self.__result }


class Code_State:
    """ The class keeps track of helper information 
        needed to track TAC stmt generation """

    def __init__(self, func: str) -> None:
        self.__func_name: str = func
        self.__temps: dict = []
        self.__temp_counter: int = 0
        self.__temps_by_scope: List = []
        self.__labels: list = []
        self.__label_counter: int = []
        self.__break_stack = []
        self.__continue_stack = []

    def __getitem__(self, jump: str) -> str:
        """ Returns label for jump statement """
        if jump == 'break':
            return self.__break_stack[-1]
        else:
            return self.__continue_stack[-1]

    def __check_scope(self, variable: ExpressionVar) -> None:
        if len(self.__temps_by_scope) == 0:
            raise RuntimeError(f'Variable {variable} is defined out of scope')

    def generate_new_temp(self) -> str:
        """ Creates and returns a new temp """
        temp = f'%{self.__temp_counter}'
        self.__temp_counter += 1
        self.__temps.append(temp)
        return temp

    def fetch_temp(self, variable: ExpressionVar) -> str:
        """ Returns a temp if it exists otherwise creates and returns one """
        self.__check_scope(variable)
        # We traverse the scopes from the last to check if variable is defined bottom up
        for scope in self.__temps_by_scope[::-1]:
            if variable.name in scope:
                return scope[variable.name]
        # otherwise we create a new temp and add it in the innermost scope
        else:
            temp = self.generate_new_temp()
            self.__temps_by_scope[-1][variable.name] = temp
            return temp
    
    def add_variable(self, variable: ExpressionVar) -> str:
        """ adds a temporary for the vardecl in code """
        self.__check_scope(variable)
        temp = self.generate_new_temp()
        self.__temps_by_scope[-1][variable.name] = temp
        return temp

    def generate_label(self) -> str:
        """ generates a new label """
        label = f'%.L{self.__label_counter}'
        self.__label_counter += 1
        self.__labels.append(label)
        return label

    def enter_scope(self) -> None:
        """ adds a new scope dict to the stack """
        self.__temps_by_scope.append({})

    def exit_scope(self) -> None:
        """ pops the last scope dict from the stack """
        self.__temps_by_scope.pop()

    def enter_loop(self, Lstart: str, Lend: str) -> None:
        """ adds respective lables to break and continue stack """
        self.__break_stack.append(Lend)
        self.__continue_stack.append(Lstart)

    def exit_loop(self) -> None:
        """ pops labels from break and continue stack """
        self.__break_stack.pop()
        self.__continue_stack.pop()

    def get_labels(self) -> list:
        return self.__labels

    def get_temps(self) -> list:
        return self.__temps

    
# ------------------------------------------------------------------------------#
# Typed Maximul Munch Class
# ------------------------------------------------------------------------------#

class AST_to_TAC_Generator:
    """ Takes the AST tree and converts it to TAC """
    def __init__(self, tree: DeclProc):
        self.__code_state: Code_State = Code_State("main")
        self.__code: DeclProc = tree
        self.__instructions: List[TAC_line] = []
        self.__macros: Code_Macro = Code_Macro
        self.__tmm_statement_parse(self.__code.get_body())

    def __emit(self, instr: TAC_line) -> None:
        self.__instructions.append(instr)

    def tac_generator(self) -> json:
        """ Generates the tac file """
        return {"proc": '@'+self.__code.get_name(),
                "body": [instr.format() for instr in self.__instructions],
                "temps": self.__code_state.get_temps(),
                "labels": self.__code_state.get_labels()}

    def __tmm_statement_parse(self, statement) -> None:
        """ parses the statement and builds its tac """
        if isinstance(statement, StatementBlock):
            self.__code_state.enter_scope()
            for stmt in statement:
                self.__tmm_statement_parse(stmt)
            self.__code_state.exit_scope() 

        elif isinstance(statement, StatementWhile):
            Lstart = self.__code_state.generate_label()
            Lbody = self.__code_state.generate_label()
            Lend = self.__code_state.generate_label()
            # treat the while loop condition
            self.__code_state.enter_loop(Lstart, Lend)
            self.__emit(TAC_line(opcode="label", args=[Lstart], result=None))
            self.__tmm_bool_expression_parse(statement.condition)
            # treat the body of while loop
            self.__emit(TAC_line(opcode="label", args=[Lbody], result=None))
            self.__tmm_statement_parse(statement.block)
            self.__emit(TAC_line(opcode="jmp", args=[Lstart], result=None))
            # treat while loop ending
            self.__emit(TAC_line(opcode="label", args=[Lend], result=None))
            self.__code_state.exit_loop()

        elif isinstance(statement, StatementIfElse):
            Ltrue = self.__code_state.generate_label()
            Lfalse = self.__code_state.generate_label()
            Lover = self.__code_state.generate_label()
            # treat condition of if stmt
            self.__tmm_bool_expression_parse(statement.condition, Ltrue, Lfalse)
            self.__emit(TAC_line(opcode="label", args=[Ltrue], result=None))
            # treat block of if stmt
            self.__tmm_statement_parse(statement.block)
            self.__emit(TAC_line(opcode="jmp", args=[Lover], result=None))
            self.__emit(TAC_line(opcode="label", args=[Lfalse], result=None))
            # treat else part if exists
            if statement.if_rest is not None: self.__tmm_statement_parse(statement.if_rest)
            self.__emit(TAC_line(opcode="jmp", args=[Lover], result=None))

        elif isinstance(statement, StatementJump):
            Ldestination = self.__code_state[statement.keyword]     # get the relevant label for jmp
            self.__emit(TAC_line(opcode="jmp", args=[Ldestination], result=None))

        elif isinstance(statement, StatementVardecl):
            temp = self.__code_state.add_variable(statement.variable)
            self.__tmm_int_expression_parse(statement.init, temp)

        elif isinstance(statement, StatementAssign):
            temp = self.__code_state.generate_new_temp()
            self.__tmm_int_expression_parse(statement.rvalue, temp)

        elif isinstance(statement, StatementPrint):
            temp = self.__code_state.fetch_temp(statement.argument)
            self.__tmm_int_expression_parse(statement.argument)
            self.__emit(TAC_line(opcode="print", args=[temp], result=None))

        else:       # should never reach here
            raise RuntimeError(f'Got unexpected statement {statement}')

    def __tmm_int_expression_parse(self, expression: Expression, temporary: str) -> None:
        """ parses the expression and builds its tac """
        if expression.type != INT:
            raise RuntimeError(f'Expression must have type INT but has type {expression.type}')
        
        if isinstance(expression, ExpressionInt):
            pass

        elif isinstance(expression, ExpressionVar):
            pass

        elif isinstance(expression, ExpressionOp):
            pass

    def __tmm_bool_expression_parse(self, expression: Expression, Ltrue: str, Lfalse: str) -> None:
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

    ast_: DeclProc = lexer_parser.run_parser(code)          # run lexer and parser
    if ast_ is None: 
        raise SyntaxError("Could not compile ast")          # exit if error occured while parsing 
    ast_.type_check()                                       # check syntax
    print('reached tac json')
    tac_ = AST_to_TAC_Generator(ast_)   # convert ast code to json
    print("tac json created")
    tac_filename = filename[:-2] + 'tac.json'   # get new file name
    with open(tac_filename, 'w') as fp:         # save the file
        json.dump(tac_.tac_generator(), fp, indent=3)
