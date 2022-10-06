from tkinter.messagebox import NO
from typing import List, Tuple, Dict

_binops_int: tuple = ("addition", "substraction", "multiplication",
                    "division", "modulus", "bitwise-and", "bitwise-or", 
                    "bitwise-xor", "logical-shift-left", "logical-shift-right")
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
    class INT: 
        """ Class of INT type """
        def __str__(self) -> str:
            return "int"

    class BOOL: 
        """ Class of BOOL type """
        def __str__(self) -> str:
            return "bool"

INT = BX_TYPE.INT
BOOL = BX_TYPE.BOOL

class Scope:
    def __init__(self) -> None:
        self.__scope_map: List[Dict[str, BX_TYPE]] = []

    def scope_len(self) -> int:
        """ returns number of scopes """
        return len(self.__scope_map)

    def create_scope(self) -> None:
        """ appends a new scope when a block is entered"""
        self.__scope_map.append({})

    def delete_scope(self) -> None:
        """ pops a scope when exiting a block """
        self.__scope_map.pop()

    def exists(self, variable: str) -> bool:
        """ Checks if a variable exists in current scope """
        return variable in self.__scope_map[-1]

    def add(self, variable: str, value: BX_TYPE) -> None:
        """ Adds a variable in the current scope """
        if self.scope_len() and self.exists(variable):
            self.__scope_map[-1][variable] = value


# ------------------------------------------------------------------------------#
# Top Classes
# ------------------------------------------------------------------------------#

import copy

class Node:
    def __init__(self, location):
        self.location = location
    def __repr__(self):
        return self.__str__()
    def syntax_error(self,error):
        msg = f"\033[0;37m in line {self.location[0]}\n {error}"
        raise SyntaxError(msg)

class DeclProc(Node):
    def __init__(self,location, name, arguments,returntype,body, previous_functions = []):
        super().__init__(location)
        self.__name = name
        self.__arguments = arguments
        self.returntype = returntype
        self.__body = body
        self.__scope = Scope()
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if self.__name != "main":
            self.syntax_error("non-main function found")
        if self.__arguments != []:
            self.syntax_error(" main function cannot have arguments")
        if self.returntype != None:
            self.syntax_error(" main function cannot have a return type")
        for statement in self.__body:
            statement.type_check(self.__scope)
    
    def __str__(self):
        return "proc(%s,%s,%s,%s)" % (self.__name, self.__arguments, self.returntype, self.__body)


# ------------------------------------------------------------------------------#
# Expression Classes
# ------------------------------------------------------------------------------#

class Expression(Node):
    def __init__(self,location):
        super().__init__(location)

class ExpressionBool(Expression):
    def __init__(self,location, value):
        super().__init__(location)
        self.value = value
        self.type = BOOL

    def __str__(self):
        return "bool(%s)" % (self.value)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:   # We should never reach here
        if self.value not in ("true", "false"):
            self.syntax_error(f"{self.value} value must be 'true' or 'false'.")

class ExpressionVar(Expression):
    def __init__(self, location: List[int], name):
        super().__init__(location)
        
        self.name = name

    def __str__(self):
        return "ExpressionVar({})".format(self.name)

    def type_check(self, scope: Scope) -> None:
        if self.name not in self.declared_ids:
            self.syntax_error(" variable yet not declared")

class ExpressionInt(Expression):
    def __init__(self, location: List[int], value):
        super().__init__(location)
        self.value = value
        self._max = 1<<63
        self.type = INT

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
        self._type_init()
    
    def __str__(self):
        return "ExpressionOp(%s,%s)" % (self.operator,self.arguments)

    def _type_init(self) -> None:
        """ Initializes the result and argument type based on argument input """
        if self.operator in _binops_int:
            self.expected_argument_type = (INT, INT)
            self.type = INT
        
        elif self.operator in _binops_bool:
            self.expected_argument_type = (BOOL, BOOL)
            self.type = BOOL

        elif self.operator in _binops_cmp:
            self.expected_argument_type = (INT, INT)
            self.type = BOOL
        
        elif self.operator in _unops_int:
            self.expected_argument_type = (INT,)
            self.type = INT

        elif self.operator in _unops_bool:
            self.expected_argument_type = (BOOL,)
            self.type = BOOL

        else:       # this should not happen
            self.syntax_error(f"Unkown operator {self.operator}")


    def type_check(self, scope: Scope) -> None:
        if len(self.arguments) != len(self.expected_argument_type):
            self.syntax_error(f"{self.operator} takes {len(self.expected_argument_type)} \
                                arguments got {len(self.arguments)}")

        for index, arg in enumerate(self.arguments):
            arg.type_check(scope)
            arg_type = self.arguments[index].type
            expected_type = self.expected_argument_type[index]
            if arg_type != expected_type:
                self.syntax_error(f"Argument {index+1} for operation {self.operator} should \
                                    have type {expected_type} but has {arg_type}")

        
# ------------------------------------------------------------------------------#
# Statement Classes
# ------------------------------------------------------------------------------#

class Statement(Node):
    def __init__(self,location):
        super().__init__(location)

class StatementBlock(Statement):
    def __init__(self,location, statements):
        super().__init__(location)
        self.statements = statements
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        scope.create_scope()
        for statement in self.statements:
            statement.type_check(scope, ongoingloop)
        scope.delete_scope()

    def __str__(self):
        return "block(%s)" % (self.statements)

class StatementVardecl(Statement):
    def __init__(self,location, name, type: BX_TYPE, init: Expression):
        super().__init__(location)
        self.name = name
        self.type: BX_TYPE = type
        self.init: Expression = init 
    
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.name,self.ty,self.init)

    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if self.type != INT:    # shouldn't be possible but anyways
            self.syntax_error(f'{self.name} should have type {str(INT)} \
                                but has type {self.type}')
        if scope.exists(self.name):
            self.syntax_error(" variable already declared")
        else:
            scope.add(self.name, self.type)
        self.init.type_check(scope)
        
class StatementPrint(Statement):
    """Actually are are prints"""
    def __init__(self, location: List[int], argument):
        super().__init__(location)
        self.argument = argument
    
    def __str__(self):
        return "print({})".format(self.arguments)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.argument.type_check(scope)
        if self.argument.type != INT:
            self.syntax_error(f'')

class StatementAssign(Statement):
    def __init__(self, location: List[int], lvalue, rvalue):
        super().__init__(location)
        self.lvalue = lvalue
        self.rvalue = rvalue
    
    def __str__(self):
        return "StatementAssign(%s,%s)" % (self.lvalue,self.rvalue)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if not scope.exists(self.lvalue):
            self.syntax_error(f" variable not yet declared")
        self.rvalue.type_check()
        if self.lvalue.type != self.rvalue.type:
            self.syntax_error(f'')

# ------------------------------------------------------------------------------#
# Conditional Statement Classes
# ------------------------------------------------------------------------------#

class StatementIfElse(Statement):
    def __init__(self, location: List[int], condition: Expression, block, ifrest):
        super().__init__(location)
        """if_body is a block, condition is an expression"""
        self.condition: Expression = condition
        self.block = block 
        self.if_rest = ifrest
    
    def __str__(self):
        return "ifelse(%s,%s,%s)" % (self.condition,self.block,self.if_rest)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        if self.condition.type != BOOL:
            self.syntax_error(f'')
        self.condition.type_check(scope)
        self.block.type_check(scope, ongoingloop)
        if self.ifrest is not None: self.if_rest.type_check(scope, ongoingloop)

class StatementWhile(Statement):
    def __init__(self, location: List[int], condition, block):
        super().__init__(location)
        self.condition = condition
        self.block = block
    
    def __str__(self):
        return "while(%s,%s)" % (self.condition,self.block)
    
    def type_check(self, scope: Scope, ongoingloop: bool) -> None:
        self.condition.type_check(scope)
        if self.condition.type != BOOL:
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

