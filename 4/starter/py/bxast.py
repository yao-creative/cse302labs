from typing import List, Tuple, Dict, Union, Any

"""

Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

# ------------------------------------------------------------------------------#
# Macro Classes
# ------------------------------------------------------------------------------#

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

class Scope:
    def __init__(self) -> None:
        self.__scope_map: List[Dict[str, BX_TYPE]] = []

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

    def exists(self, variable: str) -> bool:
        """ Checks if a variable exists in any scope """
        # print(self.__scope_map)
        # print(variable)
        for scope in self.__scope_map[::-1]:
            if variable in scope:
                return True
        return False

    def exists_in_current_scope(self, variable: str) -> bool:
        """ Checks if a variable exists in current scope """
        # print(self.__scope_map)
        # print(variable)
        if variable in self.__scope_map[-1]:
            return True
        return False
    
    def get_global(self, name) -> Tuple[List[BX_TYPE], BX_TYPE] :
        """ Returns the type of a procedure or global variable from the global scope """
        return self.__scope_map[0][name]

    def add_proc(self, proc_name: str, in_type: List[BX_TYPE], out_type: BX_TYPE) -> None:
        """ Adds a procedure in the current global scope """
        if self.scope_len():
            self.__scope_map[0][proc_name] = (in_type, out_type)
            
    def add_variable(self, variable: str, value: BX_TYPE = BX_TYPE.INT) -> None:
        """ Adds a variable in the current scope """
        if self.scope_len():
            self.__scope_map[-1][variable] = value

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
    
    def __str__(self):
        return "ExpressionProcCall(%s, %s)" % (self.__name, self.__params)
        
    def type_check(self, scope: Scope) -> None:
        """ Checks if the procedure exists and if the parameters are of the correct type """
        # if a print call then change the call to reserved print call statement
        if self.__name == "print":
            if len(self.__params) != 1:
                self.syntax_error(" print function can have only 1 parameter")

            # check print type            
            type = self.__params[0].get_type()
            if type == BX_TYPE.BOOL:
                self.__name == "__bx_print_bool"
            elif type == BX_TYPE.INT:
                self.__name == "__bx_print_int"
            else:
                self.syntax_error(" print statement has invalid argument")
            
            # set return type and return
            self.__type = BX_TYPE.VOID
            return
        
        proc = scope.get_global(self.__name)
        if proc is None:
            self.syntax_error("Procedure '%s' is not defined." % self.__name)
        elif not isinstance(proc, Tuple[List[BX_TYPE],BX_TYPE]):
            self.syntax_error(f" procedure {self.__name} already declared in global scope but as global variable")
        else:
            in_types, out_type = scope.get_from_global_scope(self.__name)
            self.__type = out_type #set type of proc call
            
            if len(self.__params) != len(in_types): #check correct num params
                self.syntax_error(f"Procedure '{self.__name}' expects {len(in_types)} parameters, but {len(self.__params)} were given.")
                
            for i,parameter in enumerate(self.__params): #check correct parameters
                parameter.type_check(scope)
                if parameter.get_type() != in_types[i]:
                    self.syntax_error(f"Parameter {i} of procedure '{self.__name}' must be of type {in_types[i]}.")
            
class ExpressionVar(Expression):
    def __init__(self, location: List[int], name: str):
        super().__init__(location)
        self.name: str = name
        self.__type: BX_TYPE = BX_TYPE.INT        # We only allow int decl in BX

    def get_type(self) -> BX_TYPE:
        return self.__type
    
    def __str__(self):
        return "ExpressionVar({})".format(self.name)

    def type_check(self, scope: Scope) -> None:
        if not scope.exists(self.name):
            self.syntax_error(f" variable not defined")
        else:
            scope.add_variable(self.name)

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
        if self.value < 0:
            self.syntax_error(" negative number")
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
        # elif self.operator in self.operations._binops_int_bool:
        #     self.expected_argument_type = [(BX_TYPE.INT, BX_TYPE.INT),(BX_TYPE.BOOL, BX_TYPE.BOOL)]
        #     self.__type = BX_TYPE.BOOL
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
        if len(self.arguments) != len(self.expected_argument_type):
            self.syntax_error(f"{self.operator} takes {len(self.expected_argument_type)} \
                                arguments got {len(self.arguments)}")

        for index, arg in enumerate(self.arguments):
            arg.type_check(scope)
            arg_type = self.arguments[index].get_type()
            # else: 
            expected_type = self.expected_argument_type[index]
            if arg_type != expected_type:
                self.syntax_error(f"Argument {index+1} for operation {self.operator} should have type {expected_type} but has {arg_type}")

#------------------------------------------------------------
# Utility for parser
#------------------------------------------------------------

class ListVarDecl:
    def __init__(self, vars: List[ExpressionVar], ty: BX_TYPE):
        self.__vars: List[ExpressionVar] = vars 
        self.__type: BX_TYPE = ty     
    
    def __add_var(self, location: List[int], name: str, expression: Expression) -> None:
        """ helper func to append var """
        self.__vars.append(StatementVardecl(location, name, self.__type, expression))
        
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

class StatementBlock(Statement):
    def __init__(self,location: List[int], statements: List[Statement]):
        super().__init__(location)
        self.statements: List[Statement] = statements
        # print("Created BLOCK class")
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        # print("entered BLOCK type_check")
        scope.create_scope()
        for statement in self.statements:
            statement.type_check(scope, ongoingloop)
        scope.delete_scope()

    def __str__(self):
        return "block(%s)" % (self.statements)
    
class StatementEval(Statement):
    #TODO: type check The type of the result is allowed to be
    # any semantic type, including the type void, because the “result” of the evaluation is not stored.
    def __init__(self,location: List[int], expression: Expression):
        super().__init__(location)
        self.expression: Expression = expression
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.expression.type_check(scope)
        
    def __str__(self):
        return "eval(%s)" % (self.expression)
    
class StatementReturn(Statement):
    #TODO:  ensure that the full type of the procedure is known at the point where
    #you are type-checking a return statement
    #TODO: Subroutines: here, an argument to return is optional. If one is provided, it must type-check
    # against the expected type void.
    def __init__(self,location: List[int], expression: Union[ExpressionVar, ExpressionProcCall]):
        super().__init__(location)
        self.expression: Union[ExpressionVar, ExpressionProcCall] = expression
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if self.expression is not None:
            self.expression.type_check(scope)
        
    def __str__(self):
        return "return(%s)" % (self.expression)
      
class StatementVardecl(Statement):
    def __init__(self,location: List[int], variable: ExpressionVar, type: BX_TYPE, init: Expression):
        super().__init__(location)
        self.variable: ExpressionVar = variable
        self.__type: BX_TYPE = BX_TYPE.getType(type)
        self.init: Expression = init 
        self.__global = False
        
    def get_type(self) -> BX_TYPE:
        return self.__type
    
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.name,self.ty,self.init)

    def global_type_check(self, scope: Scope) -> None:
        if scope.exists_in_current_scope(self.variable.name):
            self.syntax_error(" variable already declared in current global scope")
        else:
            scope.add_variable(self.variable.name, self.__type)
        self.__global = True

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        # if self.__type != BX_TYPE.INT:    # shouldn't be possible but anyways
        #     self.syntax_error(f'{self.variable.name} should have type {str(BX_TYPE.INT)} \
        #                         but has type {self.__type}')
        self.init.type_check(scope)
        if not self.__global: 
            # first global pass already did this, only need to check declaration in non-global scope
            if scope.exists_in_current_scope(self.variable.name): 
                self.syntax_error(" variable already declared in current scope")
            else:
                scope.add_variable(self.variable.name, self.__type)
        
# class StatementPrint(Statement):
#     """Actually are prints"""
#     def __init__(self, location: List[int], argument: Expression):
#         super().__init__(location)
#         self.argument: Expression = argument
    
#     def __str__(self):
#         return "print({})".format(self.argument)
    
#     def type_check(self, scope: Scope, ongoingloop: bool) -> None:
#         self.argument.type_check(scope)
#         if self.argument.type != BX_TYPE.INT:
#             self.syntax_error(f'')

class StatementAssign(Statement):
    def __init__(self, location: List[int], lvalue: ExpressionVar, rvalue: Expression):
        super().__init__(location)
        self.lvalue: ExpressionVar = lvalue
        self.rvalue: Expression = rvalue
    
    def __str__(self):
        return "StatementAssign(%s,%s)" % (self.lvalue,self.rvalue)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if not scope.exists(self.lvalue.name):
            self.syntax_error(f" variable not yet declared")
        self.rvalue.type_check(scope)
        if self.lvalue.type != self.rvalue.type:
            self.syntax_error(f'')

# ------------------------------------------------------------------------------#
# Conditional Statement Classes
# ------------------------------------------------------------------------------#

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
        if self.condition.type != BX_TYPE.BOOL:
            self.syntax_error(f'')
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
        if self.condition.type != BX_TYPE.BOOL:
            self.syntax_error(f'')
        self.block.type_check(scope, True)

class StatementJump(Statement):
    def __init__(self, location: List[int], keyword):
        super().__init__(location)
        self.keyword = keyword
    
    def __str__(self):
        return "Jump(%s)" % (self.keyword)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if not ongoingloop:
            self.syntax_error(f'')

# ------------------------------------------------------------------------------#
# Main Classes
# ------------------------------------------------------------------------------#

class DeclProc(Node):
    def __init__(self,location: List[int], name : str, arguments: List[Param], returntype: BX_TYPE, body: StatementBlock):
        super().__init__(location)
        self.__name: str = name
        self.__arguments: List[Param] = arguments
        # print(f"__name: {name} __arguments: {arguments}")
        self.__returntype: BX_TYPE = returntype
        self.__body: StatementBlock = body
        self.__scope = Scope()
        
    def global_type_check(self, scope: Scope) -> None:
        """ Checks if the procedure is already declared in the global scope.
            If not, check if it is main and restrictions on main, then add it to the global scope.
        """
        if self.__name.startswith("__bx_"):
            self.syntax_error(" function starts with reserved keyword")
        
        proc = scope.get_global(self.__name)
        if proc is not None:
            self.syntax_error(" function already declared in current scope")
        elif not isinstance(proc, Tuple[List[BX_TYPE], BX_TYPE]):
            self.syntax_error(f" procedure {self.__name} already declared in global scope but as global variable")
        else:
            if self.__name == "main":
                if self.__arguments != []:
                    self.syntax_error(" main function cannot have arguments")
                if self.__returntype != None:
                    self.syntax_error(" main function cannot have a return type")
            scope.add_proc(self.__name, [arg.get_type() for arg in self.__arguments], self.__returntype)

    def type_check(self) -> None:

        self.__body.type_check(self.__scope, False)

        # check if the func has a return statement        
        if self.__returntype != "void":
            ret_stat = False
            for stat in self.__body.statements:
                if isinstance(stat, StatementReturn):
                    ret_stat = True
                    break
            if not ret_stat:
                self.syntax_error(f" function {self.__name} has no return statement")
    
    def __str__(self):
        return "proc(%s,%s,%s,%s)" % (self.__name, self.__arguments, self.__returntype, self.__body)

    def get_name(self) -> str:
        return self.__name

    def get_args(self) -> List[Param]:
        return self.__arguments

    def get_body(self) -> StatementBlock:
        return self.__body

class Decl(Node):
    def __init__(self,location: List[int]):
        super().__init__(location)

class Prog(Node):
    def __init__(self,location: List[int], decls: List[Union[DeclProc, StatementVardecl]]):
        super().__init__(location)
        self.__decls: List[Union[DeclProc, StatementVardecl]] = decls
        self.__scope = Scope().create_scope() #immediately initialize global scope
        
    def __str__(self):
        return "Prog(%s)" % (self.__decls)
    
    def global_type_check(self) -> None:
        """
        1) Checks that all global variables and procedures are added to global scope 
        2) Checks that main is declared and has no arguments
        (expression of global variables declarations and procedure bodies are unchecked)"""
        has_main = False
        for declaration in self.__decls:
            if isinstance(declaration, DeclProc):
                if declaration.get_name() == "main":
                    has_main = True
            declaration.global_type_check(self.__scope)
                
        if not has_main:
            self.syntax_error("No main function defined")
            
    def type_check(self) -> None:
        """Checks the var declaration expressions and procedure bodies"""
        for declaration in self.__decls:
            declaration.type_check()
