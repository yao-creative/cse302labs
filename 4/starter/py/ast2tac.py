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
        self.__scope_map: List = []
        self.__labels: List[str] = []
        self.__label_counter: int = 0
        self.__break_stack = []
        self.__continue_stack = []

    # ------------------------------------------------------------------------------#
    # variable and lable handlers

    def add_globl_var(self, variable: str) -> None:
        """ Temporary for globl var is same as its name """
        assert(len(self.__scope_map) == 1), f"global variable {variable} not defined globally "
        self.__scope_map[0][variable] = variable

    def add_variable(self, variable: str) -> str:
        """ Adds a variable in code and creates a temp for it """
        self.__check_scope(variable)
        temp = self.fresh_temp()
        self.__scope_map[-1][variable] = temp
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
        """ Returns a temp if it exists otherwise raises RuntimeError"""
        self.__check_scope(variable)
        # print(f"Scope is {self.__scope_map}")
        # print(f"Variable is {variable}")
        # We traverse the scopes from the last to check if variable is defined bottom up
        for scope in self.__scope_map[::-1]:
            # print(f"Scope is {scope}")
            if variable in scope:
                # print(f" variable = {variable} and temp = {scope[variable]}")
                return scope[variable]
        # check if variable is globally defined
        if f'@{variable}' in self.__scope_map[0]:
            return scope[f'@{variable}']
        else:
            raise RuntimeError(f"Variable {variable} accessed before definition")

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
        self.__scope_map.append({})

    def __check_scope(self, variable: ExpressionVar) -> None:
        """ Asserts that a scope exists """
        if not len(self.__scope_map):
            raise RuntimeError(f'Variable {variable} is defined out of scope')

    def exit_scope(self) -> None:
        """ pops the last scope dict from the stack """
        self.__scope_map.pop()

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
        """ Returns all tac instrs """
        return self.__global_vars + self.__global_procs

    def __emit(self, opcode: str, args: List, result: str) -> None:
        self.__proc_instructions.append({"opcode": opcode, 
                                         "args": args, 
                                         "result": result })
    # ------------------------------------------------------------------------------#
    # Convert bool result to int 

    def __bool_assign(self, fresh_temp:str, expression: ExpressionBool, temporary: str) -> None:
        """ Adds TAC instrs to convert bool expr result into int """
        LTrue = self.__code_state.fresh_label()
        LFalse = self.__code_state.fresh_label()
        self.__emit("const", [0], fresh_temp)
        # if expression is true then transfer 1 to temporary
        # otherwise jmp to false where 0 is assigned above
        self.__tmm_bool_expression_parse(expression, LTrue, LFalse)
        self.__emit("label", [LTrue], None)
        self.__emit("const", [1], fresh_temp)
        self.__emit("label", [LFalse], None)
        self.__emit("copy", [fresh_temp], temporary)

    # ------------------------------------------------------------------------------#
    # ExpressionProcCall convertor

    def __expression_call(self, expression: ExpressionProcCall, temporary: str) -> None:
        """ function that creates TAC for expression call """
        for index, param in enumerate(expression.get_params()):
            temp = self.__code_state.fresh_temp()
            if param.get_type() == BX_TYPE.BOOL:
                temp2 = self.__code_state.fresh_temp()
                self.__bool_assign(temp2, param, temp)
            else:
                self.__tmm_expression_parse(param, temp)

            self.__emit(opcode="param", args=[index+1, temp], result=None)
        res = None if expression.get_type() is BX_TYPE.VOID else temporary
        self.__emit(opcode="call", args=["@"+expression.get_name(), len(expression.get_params())], result=res)

    # ------------------------------------------------------------------------------#
    # Global Muncher

    def __tmm_global_parse(self) -> None:
        """ parses the global definition and builds its tac """
        self.__code_state.enter_scope()
        # first add all global variables
        # print(self.__code.global_decls())
        for glob_func in self.__code.global_decls():
            if isinstance(glob_func, list):
                for glob_decl in glob_func:
                    if isinstance(glob_decl, StatementVardecl):
                        var = glob_decl
                        self.__code_state.add_globl_var("@"+var.variable.name)
                        if isinstance(var.init, ExpressionBool):
                            init_val = int(var.init.value)
                        else: init_val = var.init.value
                        self.__global_vars.append({"var": "@"+var.variable.name,
                                                    "init": init_val})
        # now add all global functions
        for glob_func in self.__code.global_decls():
            if isinstance(glob_func, DeclProc):
                self.__code_state.enter_scope()
                self.__code_state.enter_new_proc()
                self.__proc_instructions = []
                # TODO create example to check that params are computed left -> right
                args = []
                for var in glob_func.get_args():
                    arg_temp = self.__code_state.add_variable(var.get_name())
                    args.append(arg_temp)

                # if glob_func.get_name() == "is_odd": 
                    # print(glob_func.get_body())
                self.__tmm_statement_parse(glob_func.get_body())
                # if last instr is not ret then add it to simplify CFG analysis
                # print(glob_func.get_name())
                # print(self.__proc_instructions)
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
                # print(stmt)
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
            temp = self.__code_state.add_variable(statement.variable.name)
            expr = statement.init
            if expr.get_type() == BX_TYPE.BOOL:
                self.__bool_assign(fresh_temp=temp, expression=expr, temporary=temporary)
            else:
                self.__tmm_expression_parse(expr, temp)

        elif isinstance(statement, StatementEval):
            temp = self.__code_state.fresh_temp()
            expr = statement.expression
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
            if expr is None:
                self.__emit(opcode="ret", args=[], result=None)
            elif isinstance(expr, ExpressionVar):
                temp = self.__code_state.fetch_temp(expr.name)
                self.__emit(opcode="ret", args=[temp], result=None)
            else:
                temporary = self.__code_state.fresh_temp()
                if expr.get_type() == BX_TYPE.BOOL:
                    temp = self.__code_state.fresh_temp()
                    self.__bool_assign(fresh_temp=temp, expression=expr, temporary=temporary)
                else:
                    self.__tmm_expression_parse(expr, temporary)
                self.__emit(opcode="ret", args=[temporary], result=None)

        else:       # should never reach here
            raise RuntimeError(f'Got unexpected statement {statement}')

    # ------------------------------------------------------------------------------#
    # Int Expression Muncher

    def __tmm_expression_parse(self, expression: Expression, temporary: str) -> None:
        """ parses the expression and builds its tac """

        if expression.get_type() == BX_TYPE.BOOL:
            raise RuntimeError(f'Expression must have type INT or VOID but has type {expression.get_type()}')

        if isinstance(expression, ExpressionInt):
            # print("const:", expression.value, temporary)
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
            self.__expression_call(expression=expression, temporary=temporary)

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

        elif isinstance(expression, ExpressionVar):
            temp = self.__code_state.fetch_temp(expression.name)
            self.__emit("jz", [temp, Lfalse], None)
            self.__emit("jmp", [Ltrue], None)

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

        elif isinstance(expression, ExpressionProcCall):
            temporary = self.__code_state.fresh_temp()
            self.__expression_call(expression, temporary)
            self.__emit("jz", [temporary, Lfalse], None)
            self.__emit("jmp", [Ltrue], None)

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
    # print(tac_instr)
    with open(tac_filename, 'w') as fp:         # save the file
        json.dump(tac_instr, fp, indent=3) #, indent=3
    print(f"tac json file {tac_filename} written")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Get method for conversion and filetype.')
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename

    ast = bx2front.get_ast(filename)
    tac_instr = ast_to_tac(ast)  # get the tac instr
    write_tacfile(filename, tac_instr)
