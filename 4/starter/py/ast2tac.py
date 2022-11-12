import sys
import json
from bxast import *
from macros import tacMacros as Macros

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

# ------------------------------------------------------------------------------#
# Helper Classes
# ------------------------------------------------------------------------------#

class CodeScope:
    """ The class keeps track of scope info 
        needed to track TAC stmt generation """

    def __init__(self) -> None:
        self.__temps: dict = []
        self.__temp_counter: int = 0
        self.__temps_by_scope: List = []
        self.__labels: List[str] = []
        self.__label_counter: int = 0
        self.__break_stack = []
        self.__continue_stack = []

    # ------------------------------------------------------------------------------#
    # variable and lable handlers

    def add_variable(self, variable: ExpressionVar) -> str:
        """ Adds a variable in code and creates a temp for it """
        self.__check_scope(variable.name)
        temp = self.fresh_temp()
        self.__temps_by_scope[-1][variable.name] = temp
        return temp

    def fresh_temp(self) -> str:
        """ Creates and returns a new temp """
        temp = f'%{self.__temp_counter}'
        self.__temp_counter += 1
        self.__temps.append(temp)
        return temp

    def fresh_label(self) -> str:
        """ generates a new label """
        label = f'%.L{self.__label_counter}'
        self.__label_counter += 1
        self.__labels.append(label)
        return label

    def fetch_temp(self, variable: str) -> str:
        """ Returns a temp if it exists otherwise creates and returns one """
        # We traverse the scopes from the last to check if variable is defined bottom up
        for scope in self.__temps_by_scope[::-1]:
            # print(f"Scope is {scope}")
            if variable in scope:
                # print(f" variable = {variable} and temp = {scope[variable]}")
                return scope[variable]
        # otherwise we create a new temp and add it in the innermost scope
        else:
            temp = self.fresh_temp()
            self.__temps_by_scope[-1][variable] = temp
            return temp

    def enter_new_proc(self) -> None:
        """ Resets label and temp handlers when a new proc is entered """
        self.__temp_counter = 0
        self.__label_counter = 0
        self.__temps = []
        self.__labels = []

    # ------------------------------------------------------------------------------#
    # scope handlers

    def enter_scope(self) -> None:
        """ adds a new scope dict to the stack """
        self.__temps_by_scope.append({})

    def __check_scope(self, variable: ExpressionVar) -> None:
        if len(self.__temps_by_scope) == 0:
            raise RuntimeError(f'Variable {variable} is defined out of scope')

    def exit_scope(self) -> None:
        """ pops the last scope dict from the stack """
        self.__temps_by_scope.pop()

    # ------------------------------------------------------------------------------#
    # loop handlers

    def enter_loop(self, Lstart: str, Lend: str) -> None:
        """ adds respective lables to break and continue stack """
        self.__break_stack.append(Lend)
        self.__continue_stack.append(Lstart)

    def __getitem__(self, jump: str) -> str:
        """ Returns label for jump statement """
        if jump == 'break':
            return self.__break_stack[-1]
        else:
            return self.__continue_stack[-1]

    def exit_loop(self) -> None:
        """ pops labels from break and continue stack """
        self.__break_stack.pop()
        self.__continue_stack.pop()

    # ------------------------------------------------------------------------------#
    # getter functions

    def get_labels(self) -> list:
        """ Return sorted list of labels because last label is used in CFG """
        return sorted(self.__labels)

    def get_temps(self) -> list:
        """ Returns sorted list of temps just in case """
        return sorted(self.__temps)


# ------------------------------------------------------------------------------#
# Typed Maximal Munch Class
# ------------------------------------------------------------------------------#

class AST_to_TAC_Generator:
    """ Takes the AST tree and converts it to TAC """
    def __init__(self, tree: Prog):
        self.__code_state: CodeScope = CodeScope()
        self.__code: Prog = tree
        self.__global_vars: List[dict] = list()
        self.__global_procs: List[dict] = list()
        self.__proc_instructions: List[dict] = []
        self.__macros: Macros = Macros
        self.__tmm_global_parse()

    # ------------------------------------------------------------------------------#
    # misc functions

    def return_tac_instr(self) -> List[dict]:
        """ Generates the tac file """
        return self.__global_vars + self.__global_procs

    def __emit(self, opcode: str, args: List, result: str) -> None:
        self.__proc_instructions.append({"opcode": opcode, 
                                         "args": args, 
                                         "result": result })

    def __bool_assign(self, fresh_temp:str, expression: ExpressionBool, temporary: str) -> None:
        """ Adds TAC instrs to convert bool expr result into int """
        LTrue = self.__code_state.fresh_label()
        LFalse = self.__code_state.fresh_label()
        self.__emit("const", [0], fresh_temp)
        self.__tmm_bool_expression_parse(expression, LTrue, LFalse)
        self.__emit("label", [LTrue], None)
        self.__emit("copy", [1], fresh_temp)
        self.__emit("label", [LFalse], None)
        self.__emit("copy", fresh_temp, temporary)

    # ------------------------------------------------------------------------------#
    # Global Muncher

    def __tmm_global_parse(self) -> None:
        """ parses the global definition and builds its tac """
        self.__code_state.enter_scope()

        for glob_func in self.__code.functions:
            if isinstance(glob_func, ListVarDecl):                
                for var in glob_func.return_vardecl_list():
                    self.__code_state.add_variable("@"+var.variable)
                    self.__global_vars.append({"var": "@"+var.variable,
                                               "init": var.init})

            elif isinstance(glob_func, DeclProc):
                self.__code_state.enter_scope()
                self.__code_state.enter_new_proc()
                self.__proc_instructions = []

                args = []
                for var in glob_func.get_args():
                    args.append("%"+var.name)
                    self.__code_state.add_variable("%"+var.name)

                self.__tmm_statement_parse(glob_func.get_body())
                # if last instr is not ret then add it to simplify CFG analysis
                if self.__proc_instructions[-1]["opcode"] != "ret":
                    self.__emit(opcode="ret", args=[], result=None)
                self.__global_procs.append({"proc":"@"+glob_func.get_name(),
                                            "args": args,
                                            "body": self.__proc_instructions,
                                            "temps": self.__code_state.get_temps(),
                                            "labels": self.__code_state.get_labels()})
                self.__code_state.exit_scope()

        self.__code_state.exit_scope()

    # ------------------------------------------------------------------------------#
    # Statement Muncher

    def __tmm_statement_parse(self, statement) -> None:
        """ parses the statement and append its tac to proc_instructions """

        if isinstance(statement, StatementBlock):
            self.__code_state.enter_scope()
            for stmt in statement.statements:
                self.__tmm_statement_parse(stmt)
            self.__code_state.exit_scope() 

        elif isinstance(statement, StatementWhile):
            Lhead = self.__code_state.fresh_label()
            Lbody = self.__code_state.fresh_label()
            Lend = self.__code_state.fresh_label()
            # treat the while loop condition
            self.__code_state.enter_loop(Lhead, Lend)
            # print(f'while head label is {Lhead}')
            self.__emit(opcode="label", args=[Lhead], result=None)
            self.__tmm_bool_expression_parse(statement.condition, Lbody, Lend)
            # treat the body of while loop
            # print(f'while body label is {Lbody}')
            self.__emit(opcode="label", args=[Lbody], result=None)
            self.__tmm_statement_parse(statement.block)
            self.__emit(opcode="jmp", args=[Lhead], result=None)
            # treat while loop ending
            # print(f'while end label is {Lend}')
            self.__emit(opcode="label", args=[Lend], result=None)
            self.__code_state.exit_loop()

        elif isinstance(statement, StatementIfElse):
            Ltrue = self.__code_state.fresh_label()
            Lfalse = self.__code_state.fresh_label()
            Lover = self.__code_state.fresh_label()
            # treat condition of if stmt
            self.__tmm_bool_expression_parse(statement.condition, Ltrue, Lfalse)
            # print(f'if true label is {Ltrue}')
            self.__emit(opcode="label", args=[Ltrue], result=None)
            # treat block of if stmt
            self.__tmm_statement_parse(statement.block)
            # print(f'if over label is {Lover}')
            self.__emit(opcode="jmp", args=[Lover], result=None)
            # print(f'if false label is {Lfalse}')
            self.__emit(opcode="label", args=[Lfalse], result=None)
            # treat else part if exists
            if statement.if_rest is not None: self.__tmm_statement_parse(statement.if_rest)
            self.__emit(opcode="label", args=[Lover], result=None)

        elif isinstance(statement, StatementJump):
            # print(f"Jump stmt is {statement.keyword}")
            Ldestination = self.__code_state[statement.keyword]     # get the relevant label for jmp
            # print(f"Jump stmt destination is {Ldestination}")
            self.__emit(opcode="jmp", args=[Ldestination], result=None)

        elif isinstance(statement, StatementVardecl):
            temp = self.__code_state.add_variable(statement.variable)
            expr = statement.init
            if expr.get_type() == BX_TYPE.BOOL:
                self.__bool_assign(fresh_temp=temp, expression=expr, temporary=temporary)
            else:
                self.__tmm_expression_parse(expr, temp)

        elif isinstance(statement, StatementAssign):
            temporary = self.__code_state.fetch_temp(statement.lvalue.name)
            if statement.rvalue.get_type() == BX_TYPE.INT:
                self.__tmm_expression_parse(statement.rvalue, temporary)
            elif statement.rvalue.get_type() == BX_TYPE.BOOL:
                temp = self.__code_state.fresh_temp()
                self.__bool_assign(temp, statement.rvalue, temporary)

        elif isinstance(statement, StatementReturn):
            expr = statement.expression
            if expr is None or isinstance(expr, ExpressionProcCall):
                self.__emit(opcode="ret", args=[], result=None)
            elif isinstance(expr, ExpressionVar):
                temp = self.__code_state.add_variable(expr.name)
                self.__emit(opcode="ret", args=[temp], result=None)
            else:
                temp = self.__code_state.fresh_temp()
                if expr.get_type() == BX_TYPE.BOOL:
                    self.__bool_assign(fresh_temp=temp, expression=expr, temporary=temporary)
                else:
                    self.__tmm_expression_parse(expr, temp)
                self.__emit(opcode="ret", args=[temp], result=None)

        else:       # should never reach here
            raise RuntimeError(f'Got unexpected statement {statement}')

    # ------------------------------------------------------------------------------#
    # Expression Muncher

    def __tmm_expression_parse(self, expression: Expression, temporary: str) -> None:
        """ parses the expression and builds its tac """

        if expression.get_type() != BX_TYPE.INT:
            raise RuntimeError(f'Expression must have type INT but has type {expression.get_type()}')

        if isinstance(expression, ExpressionInt):
            self.__emit("const", [expression.value], temporary)

        elif isinstance(expression, ExpressionVar):
            temp = self.__code_state.fetch_temp(expression.name)
            if temp != temporary:
                self.__emit("copy", [temp], temporary)

        elif isinstance(expression, ExpressionOp) and len(expression.arguments) == 1:
            opcode = self.__macros.operator_map[expression.operator]
            subexpr_target = self.__code_state.fresh_temp()
            subexpr = expression.arguments[0]
            if subexpr.get_type() == BX_TYPE.BOOL:
                self.__bool_assign(fresh_temp=subexpr_target, expression=subexpr, temporary=temporary)
            else:
                self.__tmm_expression_parse(subexpr, subexpr_target)
            self.__emit(opcode, [subexpr_target], temporary)

        elif isinstance(expression, ExpressionOp) and len(expression.arguments) == 2:
            opcode = self.__macros.operator_map[expression.operator]
            subexpr_targets = []
            for subexpr in expression.arguments: 
                target = self.__code_state.fresh_temp()
                subexpr_targets.append(target)
                if subexpr.get_type() == BX_TYPE.BOOL:
                    self.__bool_assign(fresh_temp=target, expression=subexpr, temporary=temporary)
                else:
                    self.__tmm_expression_parse(subexpr, target)
            self.__emit(opcode, subexpr_targets, temporary)

        elif isinstance(expression, ExpressionProcCall):
            for index, param in enumerate(expression.params):
                if isinstance(param, ExpressionVar):
                    temp = self.__code_state.fetch_temp(param.name)
                else:
                    temp = self.__code_state.fresh_temp()
                    # if param is bool then we need to convert its result into int
                    if param.get_type() == BX_TYPE.BOOL:
                        self.__bool_assign(temp, param, temporary)
                    else:
                        self.__tmm_expression_parse(param, temporary)
                self.__emit(opcode="param", args=[index+1, temp], result=None)
            res = None if expression.get_type() is BX_TYPE.VOID else temporary
            self.__emit(opcode="call", args=["@"+expression.name, len(expression.params)], result=res)

        else:       # should never reach here
            raise RuntimeError(f'Got unexpected expression {expression}')

    # ------------------------------------------------------------------------------#
    # Bool expression Muncher

    def __tmm_bool_expression_parse(self, expression: Expression, Ltrue: str, Lfalse: str) -> None:
        """ parses the bool expression and builds its tac """
        if expression.get_type() != BX_TYPE.BOOL:
            raise RuntimeError(f'Expression must have type BOOL but has type {expression.get_type()}')

        if isinstance(expression, ExpressionBool):
            if expression.value: 
                self.__emit("jmp", [Ltrue], None)
            else: 
                self.__emit("jmp", [Lfalse], None)

        elif isinstance(expression, ExpressionOp):
            if expression.operator == "logical-and":
                Lmid = self.__code_state.fresh_label()
                self.__tmm_bool_expression_parse(expression.arguments[0], Lmid, Lfalse)
                self.__emit("label", [Lmid], None)
                self.__tmm_bool_expression_parse(expression.arguments[1], Ltrue, Lfalse)

            elif expression.operator == "logical-or":
                Lmid = self.__code_state.fresh_label()
                self.__tmm_bool_expression_parse(expression.arguments[0], Ltrue, Lmid)
                self.__emit("label", [Lmid], None)
                self.__tmm_bool_expression_parse(expression.arguments[1], Ltrue, Lfalse)

            elif expression.operator == "not":
                self.__tmm_bool_expression_parse(expression.arguments[0], Lfalse, Ltrue)

            elif expression.operator in self.__macros.jump_map:
                subexpr_targets = [] 
                for subexpr in expression.arguments: 
                    target = self.__code_state.fresh_temp()
                    subexpr_targets.append(target)
                    self.__tmm_expression_parse(subexpr, target)
                temp_result = self.__code_state.fresh_temp()
                #e1 - e2 since assembly second argument is subtracted from first
                self.__emit("sub", subexpr_targets, temp_result)
                self.__emit(self.__macros.jump_map[expression.operator], 
                            [temp_result, Ltrue], None)
                self.__emit("jmp", [Lfalse], None)

            else:       # should never reach here
                raise RuntimeError(f'Got unexpected boolean operator {expression.operator}')

        else:       # should never reach here
            raise RuntimeError(f'Got unexpected expression {expression}')


# ------------------------------------------------------------------------------#
# Main functions
# ------------------------------------------------------------------------------#

import argparse
import bx2front

def ast_to_tac(ast: Prog) -> json:
    if ast is None: raise RuntimeError("Could not compile ast")          # exit if error occured while parsing 
    
    tac_ = AST_to_TAC_Generator(ast)   # convert ast code to json
    print("tac created")
    tac_instr = tac_.return_tac_instr()
    return tac_instr

def write_tacfile(fname: str, tac_instr: List[dict]) -> None:
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

    ast = bx2front.get_ast(filename)
    tac_instr = ast_to_tac(ast)  # get the tac instr
    write_tacfile(filename, tac_instr)
