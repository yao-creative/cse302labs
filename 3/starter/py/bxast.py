from typing import List, Tuple, Dict

_binops_int: tuple = ("addition", "substraction", "multiplication",
                    "division", "modulus", "bitwise-and", "bitwise-or", 
                    "bitwise-xor", "logical-shift-left", "logical-shift-right")
_binops_cmp_val: tuple = ("cmpl", "cmple", "cmpge", "cmpg")
_binops_cmp: tuple = ("cmpe", "cmpne")
_binops_bool: tuple = ("logical-and", "logical-or")
_binops: tuple = _binops_bool + _binops_cmp_val + _binops_cmp + _binops_int

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

class Scopes:
    pass


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
        self.name = name
        self.arguments = arguments
        self.returntype = returntype
        self.body = body
    
    def type_check(self) -> None:
        if self.name != "main":
            self.syntax_error("non-main function found")
        if self.arguments != []:
            self.syntax_error(" main function cannot have arguments")
        if self.returntype != None:
            self.syntax_error(" main function cannot have a return type")
        for statement in self.body:
            statement.type_check()
    
    def __str__(self):
        return "proc(%s,%s,%s,%s)" % (self.name,self.arguments,self.returntype,self.body)


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
    
    def type_check(self) -> None:
        if self.value not in ("true", "false"):
            self.syntax_error(" value must be 'true' or 'false'.")

class ExpressionVar(Expression):
    def __init__(self, location: List[int], name, declared_ids = []):
        super().__init__(location)
        
        self.name = name
        self.declared_ids = copy.deepcopy(declared_ids)

    def __str__(self):
        return "ExpressionVar({})".format(self.name)

    def type_check(self) -> None:
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
    
    def type_check(self) -> None:
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
        self.argument_type: Tuple[BX_TYPE] = None
        self._type_init()
    
    def __str__(self):
        return "ExpressionOp(%s,%s)" % (self.operator,self.arguments)

    def _type_init(self) -> None:
        """ Initializes the result and argument type based on argument input """
        if self.operator in _binops_int:
            self.argument_type = (INT, INT)
            self.type = INT
        
        elif self.operator in _binops_bool:
            self.argument_type = (BOOL, BOOL)
            self.type = BOOL

        elif self.operator in _binops_cmp_val:
            self.argument_type = (INT, INT)
            self.type = BOOL
        
        elif self.operator in _binops_cmp:
            self.argument_type = (None, None)
            self.type = BOOL
        
        elif self.operator in _unops_int:
            self.argument_type = (INT,)
            self.type = INT

        elif self.operator in _unops_bool:
            self.argument_type = (BOOL,)
            self.type = BOOL

        else:       # this should not happen
            self.syntax_error(f"Unkown operator {self.operator}")


    def type_check(self) -> None:
        if len(self.arguments) != len(self.argument_type):
            self.syntax_error(f"{self.operator} takes {len(self.argument_type)} arguments got {len(self.arguments)}")

        for index, arg in enumerate(self.arguments):
            expected_type = self.argument_type[index]
            # in case we have
            if not expected_type and index:
                expected_type = self.arguments[0].type
            arg.type_check()
            arg_type = self.arguments[index].type
            if not expected_type:
                expected_type = arg_type
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
    
    def type_check(self) -> None:
        for statement in self.statements:
            statement.type_check()
    
    def __str__(self):
        return "block(%s)" % (self.statements)

class StatementVardecl(Statement):
    def __init__(self,location, name, ty, init, declared_ids = []):
        super().__init__(location)
        self.name = name
        self.ty = ty
        self.init = init 
        self.declared_ids = copy.deepcopy(declared_ids)
    
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.name,self.ty,self.init)

    def type_check(self) -> None:
        if self.name in self.declared_ids:
            self.syntax_error(" variable already declared")
        self.init.type_check()
        
class StatementPrint(Statement):
    """Actually are are prints"""
    def __init__(self, location: List[int], arguments):
        super().__init__(location)
        self.arguments = arguments
    
    def __str__(self):
        return "print({})".format(self.arguments)
    
    def type_check(self) -> None:
        self.arguments.type_check()

class StatementAssign(Statement):
    def __init__(self, location: List[int], lvalue,rvalue, declared_ids = []): 
        super().__init__(location)
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.declared_ids = copy.deepcopy(declared_ids)
    
    def __str__(self):
        return "StatementAssign(%s,%s)" % (self.lvalue,self.rvalue)
    
    def type_check(self) -> None:
        if self.lvalue not in self.declared_ids:
            self.syntax_error(" variable yet not declared")
        self.rvalue.type_check()

# ------------------------------------------------------------------------------#
# Conditional Statement Classes
# ------------------------------------------------------------------------------#

class StatementIfElse(Statement):
    def __init__(self, location: List[int], condition, block, ifrest):
        super().__init__(location)
        """if_body is a block, condition is an expression"""
        self.condition = condition
        self.block = block 
        self.if_rest = ifrest
    
    def __str__(self):
        return "ifelse(%s,%s,%s)" % (self.condition,self.block,self.if_rest)
    
    def type_check(self) -> None:
        self.condition.type_check()
        self.block.type_check()
        self.if_rest.type_check()

class StatementWhile(Statement):
    def __init__(self, location: List[int], condition, block):
        super().__init__(location)
        self.condition = condition
        self.block = block
    
    def __str__(self):
        return "while(%s,%s)" % (self.condition,self.block)
    
    def type_check(self) -> None:
        self.condition.type_check()
        self.block.type_check()

class StatementJump(Statement):
    def __init__(self, location: List[int], keyword):
        super().__init__(location)
        self.keyword = keyword
    
    def __str__(self):
        return "Jump(%s)" % (self.keyword)
    
    def type_check(self) -> None:
        pass

