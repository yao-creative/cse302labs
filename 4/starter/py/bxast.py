from typing import List, Tuple, Dict, Union
from macros import Operations, BX_TYPE

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

# ------------------------------------------------------------------------------#
# Class to handle Scopes
# ------------------------------------------------------------------------------#

class Scope:
    def __init__(self) -> None:
        self.__scope_map: List[Dict[str, BX_TYPE]] = list()
        self.__global_vardecls: Dict[str, BX_TYPE] = dict()

    def __str__(self) -> str:
        return str(self.__scope_map)

    def scope_len(self) -> int:
        """ returns number of scopes """
        return len(self.__scope_map)

    def create_scope(self) -> None:
        """ appends a new scope when a block is entered"""
        # print("SCOPE CREATED")
        self.__scope_map.append({})

    def delete_scope(self) -> None:
        """ pops a scope when exiting a block """
        # print("SCOPE DELETED")
        self.__scope_map.pop()

    def get_type(self, variable: str) -> BX_TYPE:
        """ Returns the type of a variable """
        for scope in self.__scope_map[::-1]:
            if variable in scope:
                return scope[variable]
        raise RuntimeError(f"variable {variable} not defined in the operation")

    def exists(self, variable: str) -> bool:
        """ Checks if a variable exists in any scope """
        # print(self.__scope_map)
        # print(variable)
        for scope in self.__scope_map[::-1]:
            if variable in scope:
                return True
        return False

    def exists_in_current_scope(self, variable) -> bool:
        """ Checks if a variable (ExpressionVar) exists in current scope """
        # print(self.__scope_map)
        # print(variable)
        if variable in self.__scope_map[-1]:
            return True
        return False

    def add_variable(self, variable: str, ty: BX_TYPE) -> None:
        """ Adds a variable (ExpressionVar.name) in the current scope """
        # print(variable)
        if self.scope_len():
            self.__scope_map[-1][variable] = ty

    def exists_in_global_scope(self, variable: str) -> bool:
        """ Checks if a variable (ExpressionVar.name) exists in current scope """
        # print(self.__scope_map[0])
        # print(variable)
        if variable in self.__scope_map[0]:
            return True
        return False

    # ---------------------------------------------------------------------------#
    # Helpers for proc functions

    def set_proc_return_type(self, type: BX_TYPE) -> None:
        """ Sets the return type for the current proc """
        # print("set proc ret type")
        self.__proc_return_type = type

    def get_proc_return_type(self) -> BX_TYPE:
        """ Get the return type for the current proc """
        # print("got proc ret type")
        if "_Scope__proc_return_type" in self.__dict__:
            return self.__proc_return_type
        raise RuntimeError("Return Type not set for the proc")

    def unset_proc_return_type(self) -> None:
        """ Unsets the return type for the proc after exit """
        # print("unset proc ret type")
        # print(self.__dict__)
        if "_Scope__proc_return_type" in self.__dict__:
            self.__dict__.pop("__proc_return_type", "")
            return
        raise RuntimeError("Return Type not set for the proc")

    # ---------------------------------------------------------------------------#
    # Helpers for global type_check

    def get_global(self, name: str) -> Tuple[List[BX_TYPE], BX_TYPE] :
        """ Returns the type of a procedure or global variable from the global scope """
        if self.exists_in_global_scope(name):
            return self.__scope_map[0][name]
        return None

    def add_proc(self, proc_name: str, in_type: List[BX_TYPE], out_type: BX_TYPE) -> None:
        """ Adds a procedure in the current global scope """
        if self.scope_len():
            self.__scope_map[0][proc_name] = (in_type, out_type)

    def add_global_var(self, name:str, ty: BX_TYPE) -> None:
        """ Adds a global vardecl """
        self.__global_vardecls[name] = ty

    def proc_in_global_vars(self, name: str) -> bool:
        """ Checks if var is declared in global vars """
        # print(name)
        # print(self.__global_vardecls)
        if name in self.__global_vardecls:
            return True
        return False

class Node:
    def __init__(self, location: List[int]):
        self.location = location

    def __repr__(self):
        return self.__str__()

    def syntax_error(self,error):
        msg = f"\033[0;37m in line {self.location[0]} {error}"
        raise SyntaxError(msg)

# ------------------------------------------------------------------------------#
# Parameter Class
# ------------------------------------------------------------------------------#

class Param(Node):
    def __init__(self, location: List[int], name: str, ty: BX_TYPE):
        super().__init__(location)
        self.__name: str = name
        self.__type: BX_TYPE = ty

    def __str__(self):
        return f"Param({self.__name}, {self.__type})"

    def get_type(self):
        """ return type of param """
        return self.__type

    def get_name(self):
        """ return name of param """
        return self.__name

    def type_check(self, scope: Scope) -> None:
        """ Type checks if the param is already defined in scope """
        if scope.exists_in_current_scope(self.__name):
            self.syntax_error(" function param is repeated")
        else:
            scope.add_variable(self.__name, self.__type)

# ------------------------------------------------------------------------------#
# Utility Class for Parser
# ------------------------------------------------------------------------------#

class ListParams:
    def __init__(self, params: List[Param], ty: BX_TYPE):
        self.params: List[Param] = params 
        self.__type: BX_TYPE = ty

    def add_param(self, location: List[int], name: str) -> None:
        """ helper function to append param """
        self.params.append(Param(location, name, self.__type))

    def add_multi_param(self, l: List[Tuple[List[int], str]]) -> None:
        """ Adds multiple parameter locations and names to the list of parameters """
        for location, name in l:
            self.add_param(location, name)

    def return_params_list(self):
        """ return list of declared params """
        return self.params

# ------------------------------------------------------------------------------#
# Expression Classes
# ------------------------------------------------------------------------------#

class Expression(Node):
    def __init__(self,location: List[int]):
        super().__init__(location)

class ExpressionBool(Expression):
    def __init__(self,location: List[int], value: bool):
        super().__init__(location)
        self.value: bool = value
        self.__type = BX_TYPE.BOOL

    def get_type(self):
        return self.__type

    def __str__(self):
        return "ExpressionBool(%s)" % (self.value)

    def type_check(self, scope: Scope) -> None:   # We should never reach here
        if self.value not in (True, False):
            self.syntax_error(f"{self.value} value must be 'true' or 'false'.")

class ExpressionProcCall(Expression):
    def __init__(self, location: List[int], name: str, params: List[Expression]):
        super().__init__(location)
        self.__name: str = name
        self.__params: List[Expression] = params
        self.__type: BX_TYPE = None

    def get_type(self) -> BX_TYPE:
        return self.__type

    def get_params(self) -> List[Expression]:
        """ return param list """
        return self.__params

    def get_name(self) -> str:
        """ Return the name of the function """
        return self.__name

    def __str__(self):
        return "ExpressionProcCall(%s, %s)" % (self.__name, self.__params)

    def type_check(self, scope: Scope) -> None:
        """ Checks if the procedure exists and if the parameters are of the correct type """
        # if a print call then change the call to reserved print call statement
        if self.__name == "print":
            if len(self.__params) != 1:
                self.syntax_error(" print function can have only 1 parameter")

            # print("entered print call")
            # set requirements for print call
            _type = self.__params[0].type_check(scope)
            _type = self.__params[0].get_type()
            # print(type(self.__params[0]))
            # print(self.__params[0].get_type())
            if _type == BX_TYPE.BOOL: self.__name = "__bx_print_bool"
            elif _type == BX_TYPE.INT: self.__name = "__bx_print_int"
            else: self.syntax_error(" print statement has invalid argument")
            # set return type for print call
            self.__type = BX_TYPE.VOID
            return

        # print(" reached ExpreProcCall type check")
        # check type of all proc arguments
        proc = scope.get_global(self.__name)
        if proc is None:
            self.syntax_error("Procedure '%s' is not defined." % self.__name)
        elif scope.proc_in_global_vars(proc[1]):
            self.syntax_error(f" procedure {self.__name} already declared in global scope but as global variable")
        else:
            in_types, out_type = scope.get_global(self.__name)
            self.__type = out_type # set type of proc call
            # check correct num params
            if len(self.__params) != len(in_types):
                self.syntax_error(f"Procedure '{self.__name}' expects {len(in_types)} parameters, but {len(self.__params)} were given.")
            # check correct params
            for i, parameter in enumerate(self.__params):
                parameter.type_check(scope)
                if parameter.get_type() != in_types[i]:
                    self.syntax_error(f"Parameter {i} of procedure '{self.__name}' must be of type {in_types[i]}.")

class ExpressionVar(Expression):
    def __init__(self, location: List[int], name: str):
        super().__init__(location)
        self.name: str = name
        self.location = location
        self.type: BX_TYPE = None

    def get_type(self) -> None:
        return self.type

    def __str__(self):
        return "ExpressionVar({})".format(self.name)

    def type_check(self, scope: Scope) -> None:
        # print("expression var", self.name, scope)
        if not scope.exists(self.name):
            self.syntax_error(f" variable not yet declared {self.name}")
        if self.type is None:
            self.type = scope.get_type(self.name)

class ExpressionInt(Expression):
    def __init__(self, location: List[int], value):
        super().__init__(location)
        self.value = value
        self.__max = 1<<63
        self.__type = BX_TYPE.INT

    def get_type(self) -> BX_TYPE:
        return self.__type

    def __str__(self):
        return "ExpressionInt({})".format(self.value)

    def type_check(self, scope: Scope) -> None:
        if self.value >= self.__max:
            self.syntax_error(" number too large")

class ExpressionOp(Expression):
    def __init__(self, location: List[int], operator: str, arguments: List[Expression]):
        """ operator  : string of the operator
            arguments : list of expressions     """
        super().__init__(location)
        self.operator: str = operator
        self.arguments = arguments
        self.__type: BX_TYPE = None
        self.expected_argument_type: Tuple[BX_TYPE] = None
        self.operations: Operations = Operations
        self.__type_init()

    def get_type(self) -> BX_TYPE:
        return self.__type
    
    def __str__(self):
        return "ExpressionOp(%s,%s)" % (self.operator,self.arguments)

    def __type_init(self) -> None:
        """ Initializes the result and argument type based on argument input """
        if self.operator in self.operations._binops_int:
            self.expected_argument_type = (BX_TYPE.INT, BX_TYPE.INT)
            self.__type = BX_TYPE.INT
        elif self.operator in self.operations._binops_bool:
            self.expected_argument_type = (BX_TYPE.BOOL, BX_TYPE.BOOL)
            self.__type = BX_TYPE.BOOL
        elif self.operator in self.operations._binops_cmp:
            self.expected_argument_type = (BX_TYPE.INT, BX_TYPE.INT)
            self.__type = BX_TYPE.BOOL
        elif self.operator in self.operations._unops_int:
            self.expected_argument_type = (BX_TYPE.INT,)
            self.__type = BX_TYPE.INT
        elif self.operator in self.operations._unops_bool:
            self.expected_argument_type = (BX_TYPE.BOOL,)
            self.__type = BX_TYPE.BOOL
        else:       # this should not happen
            self.syntax_error(f"Unkown operator {self.operator}")

    def type_check(self, scope: Scope) -> None:
        # print(F"expression op: {self}, scope: {scope}")
        if len(self.arguments) != len(self.expected_argument_type):
            self.syntax_error(f"{self.operator} takes {len(self.expected_argument_type)} \
                                arguments got {len(self.arguments)}")

        for index, arg in enumerate(self.arguments):
            # print(f"checking arg {arg} of {self.operator}")
            arg.type_check(scope)
            if isinstance(arg, ExpressionVar):
                arg_type = scope.get_type(arg.name)
            else:
                arg_type = arg.get_type()
            # print(F"arg type {arg_type}")
            expected_type = self.expected_argument_type[index]
            if arg_type != expected_type:
                self.syntax_error(f"Argument {index+1} for operation {self.operator} should have type {expected_type} but has {arg_type}")

#------------------------------------------------------------
# Utility for parser
#------------------------------------------------------------

class ListVarDecl:
    def __init__(self, var_init_params: List[Tuple[List[int], str, Expression]], ty: BX_TYPE):
        self.__vars: List[StatementVardecl] = [] 
        self.__type: BX_TYPE = ty
        self.add_multi_var(var_init_params)

    def __add_var(self, location: List[int], name: str, expression: Expression) -> None:
        """ helper func to append var """
        # print(f"adding var {name} of type {self.__type}")
        self.__vars.append(StatementVardecl(location, ExpressionVar(location, name), self.__type, expression))
        # print(F"added var {self.__vars[-1]}")

    def add_multi_var(self, l: List[Tuple[List[int], str, Expression]]) -> None:
        """ Adds multiple parameter locations and names to the list of parameters """
        for location, name, expression in l:
            self.__add_var(location, name, expression)
    
    def return_vardecl_list(self):
        """ Return list of declared variables """
        return self.__vars

# ------------------------------------------------------------------------------#
# Statement Classes
# ------------------------------------------------------------------------------#

class Statement(Node):
    def __init__(self,location: List[int]):
        super().__init__(location)

class StatementEval(Statement):
    def __init__(self,location: List[int], expression: Expression):
        super().__init__(location)
        self.expression: Expression = expression

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        # I need this in the tac to send the expression to the right parsing function
        self.expression.type_check(scope)

    def __str__(self):
        return "eval(%s)" % (self.expression)

class StatementReturn(Statement):
    def __init__(self,location: List[int], expression: Union[ExpressionVar, ExpressionProcCall]):
        super().__init__(location)
        self.expression: Union[ExpressionVar, ExpressionProcCall] = expression

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        """ Type checks if return type matches function return type"""
        # if expression is None then it is a subroutine -> VOID
        expr_ret_type = BX_TYPE.VOID
        if self.expression is not None:
            # print(f"expression for ret is {self.expression}")
            self.expression.type_check(scope)
            expr_ret_type = self.expression.get_type()
        
        # print(expr_ret_type)
        # checks ret type of expression with proc
        ret_type = scope.get_proc_return_type()
        if ret_type != expr_ret_type:
            self.syntax_error(f" expected return type {ret_type} got {expr_ret_type}")

    def __str__(self):
        return "return(%s)" % (self.expression)

class StatementVardecl(Statement):
    def __init__(self,location: List[int], variable: ExpressionVar, type: BX_TYPE, init: Expression):
        super().__init__(location)
        self.variable: ExpressionVar = variable
        self.__type: BX_TYPE = type
        self.init: Union[ExpressionInt, ExpressionBool] = init 
        self.__global = False

    def get_type(self) -> BX_TYPE:
        return self.__type
    
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.variable,self.__type,self.init)

    def global_type_check(self, scope: Scope) -> None:
        # print(f"global variable: {self.variable}")
        if scope.exists_in_current_scope(self.variable.name):
            self.syntax_error(f" variable {self.variable.name} already declared in current global scope")
        else:
            scope.add_variable(self.variable.name, self.__type)
            scope.add_global_var(self.variable.name, self.__type)
        # global vars can only be literal check
        if not isinstance(self.init, ExpressionInt) and not isinstance(self.init, ExpressionBool):
            self.syntax_error(f"globl var {self.variable.name} should be literal")
        self.__global = True

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.init.type_check(scope)
        # print("vardecl ", self.variable.name)
        # print("scope in vardecl ", scope)
        if self.__global: 
            raise RuntimeError("Entered global Vardecl Type_checker. You should not be here")
        if scope.exists_in_current_scope(self.variable.name): 
            self.syntax_error(" variable already declared in current scope")
        else:
            # print(self.variable)
            scope.add_variable(self.variable.name, self.__type)
        if self.init.get_type() != self.get_type():
            self.syntax_error(f"type mismatch for var {self.variable.name}")

class StatementAssign(Statement):
    def __init__(self, location: List[int], lvalue: ExpressionVar, rvalue: Expression):
        super().__init__(location)
        self.lvalue: ExpressionVar = lvalue
        self.rvalue: Expression = rvalue

    def __str__(self):
        return "StatementAssign(%s,%s)" % (self.lvalue,self.rvalue)

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if not scope.exists(self.lvalue.name):
            self.syntax_error(f" variable not yet declared {self.lvalue.name}")

        self.rvalue.type_check(scope)
        self.lvalue.type_check(scope)
        if self.lvalue.get_type() != self.rvalue.get_type():
            self.syntax_error(f"type mismatch for assign of {self.rvalue}")

# ------------------------------------------------------------------------------#
# Conditional Statement Classes
# ------------------------------------------------------------------------------#

class StatementBlock(Statement):
    def __init__(self,location: List[int], statements: List[Statement]):
        super().__init__(location)
        self.statements: List[Statement] = statements
        # print("Created BLOCK class")

    def type_check(self, scope: Scope, ongoingloop: bool, args: List[Param] = None) -> None:
        # print("entered BLOCK type_check")
        scope.create_scope()
        if args is not None:
            for arg in args:
                arg.type_check(scope)
                scope.add_variable(arg.get_name(), arg.get_type())
        # print("block scope ", scope)
        for statement in self.statements:
            # print(statement)
            statement.type_check(scope, ongoingloop)
        scope.delete_scope()

    def __str__(self):
        return "block(%s)" % (self.statements)

class StatementIfElse(Statement):
    def __init__(self, location: List[int], condition: Expression, block : StatementBlock, ifrest):
        super().__init__(location)
        """if_body is a block, condition is an expression"""
        self.condition: Expression = condition
        self.block: StatementBlock = block 
        self.if_rest:  Union[StatementIfElse, StatementBlock, None] = ifrest

    def __str__(self):
        return "ifelse(%s,%s,%s)" % (self.condition,self.block,self.if_rest)

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        # print(self.condition)
        if isinstance(self.condition, ExpressionVar):
            self.condition.type_check(scope)
        if self.condition.get_type() != BX_TYPE.BOOL:
            self.syntax_error(f' conditional expression does not have bool type')
        self.condition.type_check(scope)
        self.block.type_check(scope, ongoingloop)
        if self.if_rest is not None: self.if_rest.type_check(scope, ongoingloop)

class StatementWhile(Statement):
    def __init__(self, location: List[int], condition: Expression, block: StatementBlock):
        super().__init__(location)
        self.condition: Expression = condition
        self.block: StatementBlock = block

    def __str__(self):
        return "while(%s,%s)" % (self.condition,self.block)

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.condition.type_check(scope)
        if self.condition.get_type() != BX_TYPE.BOOL:
            self.syntax_error(f'condition in while statement is not Bool type {self.condition}')
        self.block.type_check(scope, True)

class StatementJump(Statement):
    def __init__(self, location: List[int], keyword):
        super().__init__(location)
        self.keyword = keyword
    
    def __str__(self):
        return "Jump(%s)" % (self.keyword)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if not ongoingloop:
            self.syntax_error(f' bad break statement')

# ------------------------------------------------------------------------------#
# Main Classes
# ------------------------------------------------------------------------------#

class DeclProc(Node):
    def __init__(self,location: List[int], name : str, arguments: List[Param], returntype: BX_TYPE, body: StatementBlock):
        super().__init__(location)
        self.__name: str = name
        self.__arguments: List[Param] = arguments
        self.__returntype: BX_TYPE = returntype
        self.__body: StatementBlock = body

    def global_type_check(self, scope: Scope) -> None:
        """ Checks if the procedure is already declared in the global scope.
            If not, check if it is main and restrictions on main, then add it to the global scope.
        """
        if self.__name.startswith("__bx_"):
            self.syntax_error(" function starts with reserved keyword")

        # print(f"global checking {self.__name}")
        proc = scope.get_global(self.__name)
        if proc is not None:
            self.syntax_error(" function already declared in current scope")
        elif proc is not None and scope.proc_in_global_vars(proc[1]):
            self.syntax_error(f" procedure {self.__name} already declared in global scope but as global variable")
        else:
            if self.__name == "main":
                if self.__arguments != []:
                    self.syntax_error(" main function cannot have arguments")
                if self.__returntype != BX_TYPE.VOID:
                    self.syntax_error(" main function cannot have a return type")
            scope.add_proc(self.__name, [arg.get_type() for arg in self.__arguments], self.__returntype)

    def type_check(self, scope: Scope) -> None:
        """ Type checks the proc block. Sets proc return type for Return statements """
        scope.set_proc_return_type(self.__returntype)
        # print(self.__arguments)
        self.__body.type_check(scope, False, self.__arguments)
        scope.unset_proc_return_type()

        # check if the func has a return statement        
        if self.__returntype != BX_TYPE.VOID:
            ret_stat = False
            for stat in self.__body.statements:
                if isinstance(stat, StatementReturn):
                    ret_stat = True
                    break
                # if all if else statements have ret then func will always ret
                if isinstance(stat, StatementIfElse):
                    if self.__ifelse_has_ret(stat):
                        ret_stat = True
                        break

            if not ret_stat:
                self.syntax_error(f" function {self.__name} of type {self.__returntype} has no return statement")

    def __ifelse_has_ret(self, statement: StatementIfElse) -> bool:
        """ Checks if the if else statement block has return statement """
        # check if if statement has a ret
        if not self.__block_has_ret(statement.block):
            return False
        # check if other conditionals have ret
        if statement.if_rest is not None:
            # check if next to next ifrest is else
            if isinstance(statement.if_rest.if_rest, StatementBlock):
                # if it is then check both elif and else blocks here
                if self.__block_has_ret(statement.if_rest.block):
                    return self.__block_has_ret(statement.if_rest.block)
                return False
            elif not self.__ifelse_has_ret(statement.if_rest):
                return False
        return False

    def __block_has_ret(self, statement: StatementBlock):
        """ check if the ifrest block has a ret statement """
        for sub_stat in statement.statements:
            if isinstance(sub_stat, StatementIfElse):
                return self.__ifelse_has_ret(sub_stat)
            if isinstance(sub_stat, StatementReturn):
                return True        
        return False

    def __str__(self):
        return "proc(%s,%s,%s,%s)" % (self.__name, self.__arguments, self.__returntype, self.__body)

    def get_name(self) -> str:
        return self.__name

    def get_args(self) -> List[Param]:
        return self.__arguments

    def get_body(self) -> StatementBlock:
        return self.__body

class Prog(Node):
    def __init__(self,location: List[int], decls: List[Union[DeclProc, StatementVardecl]]):
        super().__init__(location)
        self.__decls: List[Union[DeclProc, StatementVardecl]] = decls
        self.__scope = Scope()
        self.__scope.create_scope() #immediately initialize global scope

    def global_decls(self) -> List[Union[DeclProc, StatementVardecl]]:
        """ Return all the global declarations """
        return self.__decls

    def __str__(self):
        return "Prog(%s)" % (self.__decls)

    def global_type_check(self) -> None:
        """ 1) Checks that all global vardecls and procs are added to global scope 
            2) Checks that main is declared and has no arguments
            (expression of global vardecls and proc bodies are unchecked)
        """
        has_main = False
        for declaration in self.__decls:
            # print(f"declaration {declaration}")
            if isinstance(declaration, DeclProc):
                if declaration.get_name() == "main":
                    has_main = True
            if isinstance(declaration, list):
                for decl in declaration:
                    # print(decl)
                    decl.global_type_check(self.__scope)
            else:
                declaration.global_type_check(self.__scope)
        if not has_main:
            self.syntax_error("No main function defined")

    def type_check(self) -> None:
        """Checks the var declaration expressions and procedure bodies"""
        for declaration in self.__decls:
            # global var decls are passed as list and they can be skipped
            if isinstance(declaration, list):
                # print(declaration)
                continue
            else:
                declaration.type_check(self.__scope)

class Decl(Node):
    def __init__(self,location: List[int]):
        super().__init__(location)