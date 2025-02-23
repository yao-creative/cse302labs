#can assume that all of the variable names are distinct
binops = ["addition", "substraction", "multiplication", "division", "modulus", "bitwise-and", "bitwise-or", "bitwise-xor", "logical-shift-left", "logical-shift-right"]
unops = [ "bitwise-negation", "opposite"]
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
    def syntax_check(self):
        if self.name != "main":
            self.syntax_error("non-main function found")
        if self.arguments != []:
            self.syntax_error("Error: main function cannot have arguments")
        if self.returntype != None:
            self.syntax_error("Error: main function cannot have a return type")
        for statement in self.body:
            statement.syntax_check()
    def __str__(self):
        return "proc(%s,%s,%s,%s)" % (self.name,self.arguments,self.returntype,self.body)
class Statement(Node):
    def __init__(self,location):
        super().__init__(location)
class StatementVardecl(Statement):
    def __init__(self,location, name, t, init, declared_ids = []):
        super().__init__(location)
        self.name = name
        self.type = t
        self.init = init 
        self.declared_ids = copy.deepcopy(declared_ids)
        # print(f"self: {self}")
        # print(F"declared_ids: {self.declared_ids}")
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.name,self.type,self.init)

    def syntax_check(self):
        # print(f"checking self: {self}")
        if self.name in self.declared_ids:
            self.syntax_error("Error: variable already declared")
        self.init.syntax_check()
        
class StatementPrint(Statement):
    """Actually are are prints"""
    def __init__(self, location, arguments):
        super().__init__(location)
        self.arguments = arguments
    def __str__(self):
        return "print({})".format(self.arguments)
    def syntax_check(self):
        self.arguments.syntax_check()
class StatementAssign(Statement):
    def __init__(self, location, lvalue,rvalue, declared_ids = []): 
        super().__init__(location)
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.declared_ids = copy.deepcopy(declared_ids)
        # print(f"self.declared_ids: {self.declared_ids} self.lvalue: {self.lvalue}")
    def __str__(self):
        return "StatementAssign(%s,%s)" % (self.lvalue,self.rvalue)
    def syntax_check(self):
        if self.lvalue not in self.declared_ids:
            self.syntax_error("Error: variable yet not declared")
        self.rvalue.syntax_check()
class Expression(Node):
    def __init__(self,location):
        super().__init__(location)

class ExpressionVar(Expression):
    def __init__(self, location, name, declared_ids = []):
        super().__init__(location)
        
        self.name = name
        self.declared_ids = copy.deepcopy(declared_ids)

    def __str__(self):
        return "ExpressionVar({})".format(self.name)

    def syntax_check(self):
        if self.name not in self.declared_ids:
            self.syntax_error("Error: variable yet not declared")
class ExpressionInt(Expression):
    def __init__(self, location, value):
        super().__init__(location)
        self.value = value
    def __str__(self):
        return "ExpressionInt({})".format(self.value)
    def syntax_check(self):
        if self.value < 0:
            self.syntax_error("Error: negative number")
        if self.value >= 2**63:
            self.syntax_error("Error: number too large")

class ExpressionOp(Expression):
    def __init__(self, location, operator, arguments):
        """operator: string of the operator
        arguments: list of expressions"""
        super().__init__(location)
        self.operator = operator
        self.arguments = arguments
    def __str__(self):
        return "ExpressionOp(%s,%s)" % (self.operator,self.arguments)

    def syntax_check(self):
        if self.operator in binops:
            if len(self.arguments) != 2:
                self.syntax_error("Error: arithmetic operator takes two arguments")
            self.arguments[0].syntax_check()
            self.arguments[1].syntax_check()
        elif self.operator in unops:
            if len(self.arguments) != 1:
                self.syntax_error("Error: negation operator takes one argument")
            self.arguments[0].syntax_check()
        else:
            self.syntax_error("Error: invalid operator")
        for arg in self.arguments:
            arg.syntax_check()