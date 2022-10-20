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

    def __init__(self) -> None:
        self.__temps: dict = []
        self.__temp_counter: int = 0
        self.__temps_by_scope: List = []
        self.__labels: list = []
        # self.__label_counter: int = 0
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

    def fetch_temp(self, variable: str) -> str:
        """ Returns a temp if it exists otherwise creates and returns one """
        # self.__check_scope(variable)
        # We traverse the scopes from the last to check if variable is defined bottom up
        for scope in self.__temps_by_scope[::-1]:
            # print(f"Scope is {scope}")
            if variable in scope:
                # print(f" variable = {variable} and temp = {scope[variable]}")
                return scope[variable]
        # otherwise we create a new temp and add it in the innermost scope
        else:
            temp = self.generate_new_temp()
            self.__temps_by_scope[-1][variable] = temp
            return temp
    
    def add_variable(self, variable: ExpressionVar) -> str:
        """ adds a temporary for the vardecl in code """
        self.__check_scope(variable.name)
        temp = self.generate_new_temp()
        self.__temps_by_scope[-1][variable.name] = temp
        return temp

    def generate_new_temp(self) -> str:
        """ Creates and returns a new temp """
        temp = f'%{self.__temp_counter}'
        self.__temp_counter += 1
        self.__temps.append(temp)
        return temp

    def generate_label(self) -> str:
        """ generates a new label """
        label = f'%.L{self.__temp_counter}'
        self.__temp_counter += 1
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
# Typed Maximal Munch Class
# ------------------------------------------------------------------------------#

class AST_to_TAC_Generator:
    """ Takes the AST tree and converts it to TAC """
    def __init__(self, tree: DeclProc):
        self.__code_state: Code_State = Code_State()
        self.__code: DeclProc = tree
        self.__instructions: List[Dict[TAC_line]] = []
        self.__macros: Code_Macro = Code_Macro
        self.__tmm_statement_parse(self.__code.get_body())

    def __emit(self, instr: TAC_line) -> None:
        self.__instructions.append(instr)

    def tac_generator(self) -> List[dict]:
        """ Generates the tac file """
        return [{"proc": '@'+self.__code.get_name(),
                "body": self.__instructions,
                "temps": self.__code_state.get_temps(),
                "labels": self.__code_state.get_labels()}]

    def __tmm_statement_parse(self, statement) -> None:
        """ parses the statement and builds its tac """
        if isinstance(statement, StatementBlock):
            self.__code_state.enter_scope()
            for stmt in statement.statements:
                self.__tmm_statement_parse(stmt)
            self.__code_state.exit_scope() 

        elif isinstance(statement, StatementWhile):
            Lhead = self.__code_state.generate_label()
            Lbody = self.__code_state.generate_label()
            Lend = self.__code_state.generate_label()
            # treat the while loop condition
            self.__code_state.enter_loop(Lhead, Lend)
            # print(f'while head label is {Lhead}')
            self.__emit(TAC_line(opcode="label", args=[Lhead], result=None).format())
            self.__tmm_bool_expression_parse(statement.condition, Lbody, Lend)
            # treat the body of while loop
            # print(f'while body label is {Lbody}')
            self.__emit(TAC_line(opcode="label", args=[Lbody], result=None).format())
            self.__tmm_statement_parse(statement.block)
            self.__emit(TAC_line(opcode="jmp", args=[Lhead], result=None).format())
            # treat while loop ending
            # print(f'while end label is {Lend}')
            self.__emit(TAC_line(opcode="label", args=[Lend], result=None).format())
            self.__code_state.exit_loop()

        elif isinstance(statement, StatementIfElse):
            Ltrue = self.__code_state.generate_label()
            Lfalse = self.__code_state.generate_label()
            Lover = self.__code_state.generate_label()
            # treat condition of if stmt
            self.__tmm_bool_expression_parse(statement.condition, Ltrue, Lfalse)
            # print(f'if true label is {Ltrue}')
            self.__emit(TAC_line(opcode="label", args=[Ltrue], result=None).format())
            # treat block of if stmt
            self.__tmm_statement_parse(statement.block)
            # print(f'if over label is {Lover}')
            self.__emit(TAC_line(opcode="jmp", args=[Lover], result=None).format())
            # print(f'if false label is {Lfalse}')
            self.__emit(TAC_line(opcode="label", args=[Lfalse], result=None).format())
            # treat else part if exists
            if statement.if_rest is not None: self.__tmm_statement_parse(statement.if_rest)
            self.__emit(TAC_line(opcode="label", args=[Lover], result=None).format())

        elif isinstance(statement, StatementJump):
            # print(f"Jump stmt is {statement.keyword}")
            Ldestination = self.__code_state[statement.keyword]     # get the relevant label for jmp
            # print(f"Jump stmt destination is {Ldestination}")
            self.__emit(TAC_line(opcode="jmp", args=[Ldestination], result=None).format())

        elif isinstance(statement, StatementVardecl):
            temp = self.__code_state.add_variable(statement.variable)
            self.__tmm_int_expression_parse(statement.init, temp)

        elif isinstance(statement, StatementAssign):
            temp = self.__code_state.fetch_temp(statement.lvalue.name)
            self.__tmm_int_expression_parse(statement.rvalue, temp)

        elif isinstance(statement, StatementPrint):
            temp = self.__code_state.generate_new_temp()
            self.__tmm_int_expression_parse(statement.argument, temp)
            self.__emit(TAC_line(opcode="print", args=[temp], result=None).format())

        else:       # should never reach here
            raise RuntimeError(f'Got unexpected statement {statement}')

    def __tmm_int_expression_parse(self, expression: Expression, temporary: str) -> None:
        """ parses the expression and builds its tac """
        
        if expression.type != BX_TYPE.INT:
            raise RuntimeError(f'Expression must have type INT but has type {expression.type}')
        
        if isinstance(expression, ExpressionInt):
            self.__emit(TAC_line("const", [expression.value], temporary).format())

        elif isinstance(expression, ExpressionVar):
            temp = self.__code_state.fetch_temp(expression.name)
            if temp != temporary:
                self.__emit(TAC_line("copy", [temp], temporary).format())

        elif isinstance(expression, ExpressionOp) and len(expression.arguments) == 1:
            opcode = self.__macros.operator_map[expression.operator]
            subexpr_target = self.__code_state.generate_new_temp()
            self.__tmm_int_expression_parse(expression.arguments[0], subexpr_target)
            self.__emit(TAC_line(opcode, [subexpr_target], temporary).format()) 
            
        elif isinstance(expression, ExpressionOp) and len(expression.arguments) == 2:
            opcode = self.__macros.operator_map[expression.operator]
            subexpr_targets = []
            for subexpr in expression.arguments: 
                target = self.__code_state.generate_new_temp()
                subexpr_targets.append(target)
                self.__tmm_int_expression_parse(subexpr, target)
            self.__emit(TAC_line(opcode, subexpr_targets, temporary).format())
        
        else:       # should never reach here
            raise RuntimeError(f'Got unexpected expression {expression}')

    def __tmm_bool_expression_parse(self, expression: Expression, Ltrue: str, Lfalse: str) -> None:
        """ parses the expression and builds its tac """
        if expression.type != BX_TYPE.BOOL:
            raise RuntimeError(f'Expression must have type BOOL but has type {expression.type}')
        
        if isinstance(expression, ExpressionBool):
            if expression.value: 
                self.__emit(TAC_line("jmp", [Ltrue], None).format())
            else: 
                self.__emit(TAC_line("jmp", [Lfalse], None).format())

        elif isinstance(expression, ExpressionOp):
            if expression.operator == "logical-and":
                Lmid = self.__code_state.generate_label()
                self.__tmm_bool_expression_parse(expression.arguments[0], Lmid, Lfalse)
                self.__emit(TAC_line("label", [Lmid], None).format())
                self.__tmm_bool_expression_parse(expression.arguments[1], Ltrue, Lfalse)
                
            elif expression.operator == "logical-or":
                Lmid = self.__code_state.generate_label()
                self.__tmm_bool_expression_parse(expression.arguments[0], Ltrue, Lmid)
                self.__emit(TAC_line("label", [Lmid], None).format())
                self.__tmm_bool_expression_parse(expression.arguments[1], Ltrue, Lfalse)
                
            elif expression.operator == "not":
                self.__tmm_bool_expression_parse(expression.arguments[0], Lfalse, Ltrue)
                
            elif expression.operator in self.__macros.jump_map:
                subexpr_targets = [] 
                for subexpr in expression.arguments: 
                    target = self.__code_state.generate_new_temp()
                    subexpr_targets.append(target)
                    self.__tmm_int_expression_parse(subexpr, target)
                temp_result = self.__code_state.generate_new_temp()
                self.__emit(TAC_line("sub", subexpr_targets, temp_result).format())
                #e1 - e2 since assembly second argument is subtracted from first
                self.__emit(TAC_line(self.__macros.jump_map[expression.operator], 
                                    [temp_result, Ltrue], None).format())
                self.__emit(TAC_line("jmp", [Lfalse], None).format())
        
            else:
                raise RuntimeError(f'Got unexpected boolean operator {expression.operator}')
            
        else:       # should never reach here
            raise RuntimeError(f'Got unexpected expression {expression}')
            


# ------------------------------------------------------------------------------#
# Main function
# ------------------------------------------------------------------------------#

import argparse
import my_parser as lexer_parser

def source_to_tac(filename: str) -> json:
    ast_: DeclProc = lexer_parser.run_parser(filename)          # run lexer and parser
    if ast_ is None: 
        raise SyntaxError("Could not compile ast")          # exit if error occured while parsing 
    
    ast_.type_check()                                       # check syntax
    print('reached tac json')
    tac_ = AST_to_TAC_Generator(ast_)   # convert ast code to json
    print("tac object created")

    return tac_

def write_tacfile(fname: str, tac_instr: List) -> None:
    """ Writes a tac json to the system """
    tac_filename = fname[:-2] + 'tac.json'   # get new file name
    with open(tac_filename, 'w') as fp:         # save the file
        json.dump(tac_instr, fp) #, indent=3
    print(f"tac json file {tac_filename} written")


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Get method for conversion and filetype.')
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename

    tac_instr = source_to_tac(filename)  # get the tac instr

    write_tacfile(filename, tac_instr)
