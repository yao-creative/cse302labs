from typing import List, Tuple, Dict, Union, Any

"""
NOTE FOR THE GRADER:

For comparison operators != and == we have only implemented INT
comparisons and not BOOL comparisons as stated in the assignment.
In this regards, the file ../examples/boolops.bx throws an error
as it implements bool comparisons in line 18 which is not allowed
by our compiler. Thank you for taking this into account.

Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

class Operations:
    """ A class that declares all operations for global use """
    _binops_int: tuple = ("addition", "substraction", "multiplication",
                        "division", "modulus", "bitwise-and", "bitwise-or", 
                        "bitwise-xor", "logical-shift-left", "logical-shift-right")
    # _binops_int_bool: tuple = ("cmpe", "cmpne")
    #_binops_cmp: tuple = ("cmpl", "cmple", "cmpge", "cmpg") delete line below
    _binops_cmp: tuple = ("cmpl", "cmple", "cmpge", "cmpg", "cmpe", "cmpne")
    _binops_bool: tuple = ("logical-and", "logical-or")
    _binops: tuple = _binops_bool + _binops_cmp + _binops_int

    _unops_int: tuple = ("bitwise-negation", "opposite")
    _unops_bool: tuple = ("not",)
    _unops: tuple = _unops_bool + _unops_int

# ------------------------------------------------------------------------------#
# Macro Classes
# ------------------------------------------------------------------------------#

class BX_TYPE:
    """ Class of all the data types in BX """

    def getType(__name: str) -> Any:
        if __name == "int":
            return BX_TYPE.INT
        elif __name == "bool":
            return BX_TYPE.BOOL

    class INT: 
        """ Class of INT type """
        def __str__(self) -> str:
            return "int"

    class BOOL: 
        """ Class of BOOL type """
        def __str__(self) -> str:
            return "bool"

        # def __getitem__(type) -> str:
        #     if type == "True":
        #         return "true"
        #     else: return "false"

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

    def add(self, variable: str, value: BX_TYPE = BX_TYPE.INT) -> None:
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
# Expression Classes
# ------------------------------------------------------------------------------#
class Param(Node):
    def __init__(self, location: List[int], name: str, ty: BX_TYPE):
        super().__init__(location)
        self.name: str = name
        self.type: BX_TYPE = ty     
class ListParams:
    def __init__(self, params: List[Param], ty: BX_TYPE):
        self.params: List[Param] = params 
        self.type: BX_TYPE = ty     
    def add_param(self, location: List[int], name: str) -> None:
        self.params.append(Param(location, name, self.type))
        
    def add_multi_param(self, l: List[Tuple[List[int], str]]) -> None:
        """ Adds multiple parameter locations and names to the list of parameters """
        for location, name in l:
            self.add_param(location, name)
    def return_params_list(self):
        return self.params

class Expression(Node):
    def __init__(self,location: List[int]):
        super().__init__(location)

class ExpressionBool(Expression):
    def __init__(self,location: List[int], value: bool):
        super().__init__(location)
        self.value: bool = value
        self.type = BX_TYPE.BOOL

    def __str__(self):
        return "ExpressionBool(%s)" % (self.value)
    
    def type_check(self, scope: Scope) -> None:   # We should never reach here
        if self.value not in (True, False):
            self.syntax_error(f"{self.value} value must be 'true' or 'false'.")
            
class ExpressionProcCall(Expression):
    def __init__(self, location: List[int], name: str, params: List[Expression]):
        super().__init__(location)
        self.name: str = name
        self.params: List[Expression] = params
        self.type = None
    def __str__(self):
        return "ExpressionProcCall(%s, %s)" % (self.name, self.params)
    def type_check(self, scope: Scope) -> None:
        pass
            
class ExpressionVar(Expression):
    def __init__(self, location: List[int], name: str):
        super().__init__(location)
        self.name: str = name
        self.type: BX_TYPE = BX_TYPE.INT        # We only allow int decl in BX

    def __str__(self):
        return "ExpressionVar({})".format(self.name)

    def type_check(self, scope: Scope) -> None:
        if not scope.exists(self.name):
            self.syntax_error(f" variable not defined")
        else:
            scope.add(self.name)

class ExpressionInt(Expression):
    def __init__(self, location: List[int], value):
        super().__init__(location)
        self.value = value
        self._max = 1<<63
        self.type = BX_TYPE.INT

    def __str__(self):
        return "ExpressionInt({})".format(self.value)
    
    def type_check(self, scope: Scope) -> None:
        if self.value < 0:
            self.syntax_error(" negative number")
        if self.value >= self._max:
            self.syntax_error(" number too large")

class ExpressionOp(Expression):
    def __init__(self, location: List[int], operator: str, arguments: List[Expression]):
        """ operator  : string of the operator
            arguments : list of expressions     """
        super().__init__(location)
        self.operator: str = operator
        self.arguments = arguments
        self.type: BX_TYPE = None
        self.expected_argument_type: Tuple[BX_TYPE] = None
        self.operations: Operations = Operations
        self._type_init()
    
    def __str__(self):
        return "ExpressionOp(%s,%s)" % (self.operator,self.arguments)

    def _type_init(self) -> None:
        """ Initializes the result and argument type based on argument input """
        if self.operator in self.operations._binops_int:
            self.expected_argument_type = (BX_TYPE.INT, BX_TYPE.INT)
            self.type = BX_TYPE.INT
        # elif self.operator in self.operations._binops_int_bool:
        #     self.expected_argument_type = [(BX_TYPE.INT, BX_TYPE.INT),(BX_TYPE.BOOL, BX_TYPE.BOOL)]
        #     self.type = BX_TYPE.BOOL
        elif self.operator in self.operations._binops_bool:
            self.expected_argument_type = (BX_TYPE.BOOL, BX_TYPE.BOOL)
            self.type = BX_TYPE.BOOL

        elif self.operator in self.operations._binops_cmp:
            self.expected_argument_type = (BX_TYPE.INT, BX_TYPE.INT)
            self.type = BX_TYPE.BOOL
        
        elif self.operator in self.operations._unops_int:
            self.expected_argument_type = (BX_TYPE.INT,)
            self.type = BX_TYPE.INT
        
        elif self.operator in self.operations._unops_bool:
            self.expected_argument_type = (BX_TYPE.BOOL,)
            self.type = BX_TYPE.BOOL

        else:       # this should not happen
            self.syntax_error(f"Unkown operator {self.operator}")


    def type_check(self, scope: Scope) -> None:
        if len(self.arguments) != len(self.expected_argument_type):
            self.syntax_error(f"{self.operator} takes {len(self.expected_argument_type)} \
                                arguments got {len(self.arguments)}")
        # real_expected_type = [None] * len(self.arguments)
        for index, arg in enumerate(self.arguments):
            arg.type_check(scope)
            arg_type = self.arguments[index].type
            # else: 
            expected_type = self.expected_argument_type[index]
            if arg_type != expected_type:
                self.syntax_error(f"Argument {index+1} for operation {self.operator} should have type {expected_type} but has {arg_type}")
class ListVarDecl:
    def __init__(self, vars: List[ExpressionVar], ty: BX_TYPE):
        self.vars: List[ExpressionVar] = vars 
        self.type: BX_TYPE = ty     
        
    def add_var(self, location: List[int], name: str, expression: Expression) -> None:
        self.vars.append(StatementVardecl(location, name, self.type, expression))
        
    def add_multi_var(self, l: List[Tuple[List[int], str, Expression]]) -> None:
        """ Adds multiple parameter locations and names to the list of parameters """
        for location, name, expression in l:
            self.add_var(location, name, expression)
    def return_vardecl_list(self):
        return self.vars                

       
        
# ------------------------------------------------------------------------------#
# Statement Classes
# ------------------------------------------------------------------------------#
class Prog(Node):
    def __init__(self,location: List[int], functions: List[str]):
        super().__init__(location)
        self.functions: List[str] = functions
    def __str__(self):
        return "Prog(%s)" % (self.functions)
class Decl(Node):
    def __init__(self,location: List[int]):
        super().__init__(location)
        
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
    def __init__(self,location: List[int], expression: Expression):
        super().__init__(location)
        self.expression: Expression = expression
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.expression.type_check(scope)
        
    def __str__(self):
        return "eval(%s)" % (self.expression)
    
class StatementReturn(Statement):
    def __init__(self,location: List[int], expression: Expression):
        super().__init__(location)
        self.expression: Expression = expression
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if self.expression is not None:
            self.expression.type_check(scope)
        
    def __str__(self):
        return "return(%s)" % (self.expression)
      
class StatementVardecl(Statement):
    def __init__(self,location: List[int], variable: ExpressionVar, type: BX_TYPE, init: Expression):
        super().__init__(location)
        self.variable: ExpressionVar = variable
        self.type: BX_TYPE = BX_TYPE.getType(type)
        self.init: Expression = init 
    
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.name,self.ty,self.init)

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if self.type != BX_TYPE.INT:    # shouldn't be possible but anyways
            self.syntax_error(f'{self.variable.name} should have type {str(BX_TYPE.INT)} \
                                but has type {self.type}')
        # print("Entered vardecl typecheck")
        # print(f"{self.variable}")
        # print(f"{self.variable.name}")
        self.init.type_check(scope)
        if scope.exists_in_current_scope(self.variable.name):
            self.syntax_error(" variable already declared in current scope")
        else:
            scope.add(self.variable.name, self.type)
        
class StatementPrint(Statement):
    """Actually are prints"""
    def __init__(self, location: List[int], argument: Expression):
        super().__init__(location)
        self.argument: Expression = argument
    
    def __str__(self):
        return "print({})".format(self.argument)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.argument.type_check(scope)
        if self.argument.type != BX_TYPE.INT:
            self.syntax_error(f'')

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
# Main Class
# ------------------------------------------------------------------------------#

class DeclProc(Node):
    def __init__(self,location: List[int], name : str, arguments: List[Param], returntype: type, body: StatementBlock):
        super().__init__(location)
        self.__name: str = name
        self.__arguments: List[Param] = arguments
        # print(f"__name: {name} __arguments: {arguments}")
        self.__returntype: type = returntype
        self.__body: StatementBlock = body
        self.__scope = Scope()
    
    def type_check(self) -> None:
        if self.__name != "main":
            self.syntax_error("non-main function found")
        if self.__arguments != []:
            self.syntax_error(" main function cannot have arguments")
        if self.__returntype != None:
            self.syntax_error(" main function cannot have a return type")
        self.__body.type_check(self.__scope, False)
    
    def __str__(self):
        print(f"string declproc")
        return "proc(%s,%s,%s,%s)" % (self.__name, self.__arguments, self.__returntype, self.__body)

    def get_name(self) -> str:
        return self.__name

    def get_body(self) -> StatementBlock:
        return self.__body
