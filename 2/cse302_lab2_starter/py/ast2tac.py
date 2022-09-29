from re import search
import sys
import json
from bxast import *

class TAC_proc:
    def __init__(self, tree, mm):
        print(f"initializing TAC_proc")
        self.proc = f"@{tree.name}"
        self.body = []
        self.tree = tree
        self.temps = {}
        self.operator_map = {
            "substraction": "sub",
            "addition": "add",
            "multiplication": "mul",
            "division": "div",
            "modulus": "mod",
            "bitwise-and": "and",
            "bitwise-or": "or",
            "bitwise-xor": "xor",
            "bitwise-negation": "not",
            "logical-shift-right": "shr",
            "logical-shift-left": "shl",
            "opposite": "neg",
        }
        if mm == "--tmm":
            self.tmm()
        elif mm == "--bmm":
            self.bmm()
        
    def new_temp(self, key=None):
        if key not in self.temps:
            self.temps[key] = f"%{len(self.temps)}"
        return self.temps[key]
    def search(self, key):
        """Searches for a key in the temps dictionary"""
        if key in self.temps:
            return True
        else:
            return False
    def save(self,outfile):
        with open(outfile, 'w') as fp:
            json.dump([{"proc": self.proc, "body": self.body}], fp)

    #___________________________________________________________
    #TMM
    #___________________________________________________________
    def tmm_stmt(self,statement):
        """Takes a statement and returns a list of TAC statements"""
        if isinstance(statement, StatementVardecl):
            result = self.new_temp(statement.name)
            return self.tmm_expr(statement.init,result) 
        elif isinstance(statement, StatementPrint):
            temp_to_print = self.new_temp(f"{len(self.temps)}")
            #this is guaranteed unique since it is an integer and length keeps growing.
            prev_lines = self.tmm_expr(statement.arguments, temp_to_print)
            opcode = "print"
            result = None
            return prev_lines + [TAC_line(opcode, [temp_to_print], result).format()]
        elif isinstance(statement, StatementAssign):
            result = self.new_temp(statement.lvalue)
            return self.tmm_expr(statement.rvalue,result)
            
            
    def tmm_expr(self,expression,result):
        """Takes an expression and returns a list of TAC statements"""
        if isinstance(expression, ExpressionInt):
            opcode = "const"
            args = [expression.value] #what if two intergers same name?
            return [TAC_line(opcode, args, result).format()]
        elif isinstance(expression, ExpressionVar):
            opcode = "copy"
            args = [self.temps[expression.name]]
            return [TAC_line(opcode, args, result).format()]
            #This expression is unary or binary operator
        elif isinstance(expression, ExpressionOp) and len(expression.arguments) == 1:
            #unary operator
            opcode = self.operator_map[expression.operator]
            subexpr_target = self.new_temp(f"{len(self.temps)}")
            prev_lines = self.tmm_expr(expression.arguments[0], subexpr_target)
            return prev_lines + [TAC_line(opcode, [subexpr_target], result).format()] #figure out args from last one
        else:   #binary operator
            prev_lines = []
            opcode = self.operator_map[expression.operator]
            subexpr_targets = [] #the two subexpressions are fed into the higher one, the binary operator expression
            for subexpr in expression.arguments: 
                target = self.new_temp(f"{len(self.temps)}")
                subexpr_targets.append(target)
                prev_lines += self.tmm_expr(subexpr,target)
            return prev_lines + [TAC_line(opcode, subexpr_targets, result).format()] #figure out args are last two
        
    def tmm(self):
        print(f"tmm")
        for item in self.tree.body:
            print(f"item: {item}")
            self.body += self.tmm_stmt(item)
        # print(f"body: {self.body}")
        
    #___________________________________________________________
    #BMM
    #___________________________________________________________
    def bmm_stmt(self,statement):
        """Takes a statement and returns a list of TAC statements"""
        if isinstance(statement, StatementVardecl):
            prev_lines, expr_result = self.bmm_expr(statement.init)
            result = self.new_temp(statement.name)
            return prev_lines + [TAC_line("copy", [expr_result], result).format()]
        elif isinstance(statement, StatementPrint):
            #this is guaranteed unique since it is an integer and length keeps growing.
            prev_lines,temp_to_print = self.bmm_expr(statement.arguments)
            opcode = "print"
            result = None
            return prev_lines + [TAC_line(opcode, [temp_to_print], result).format()]
        elif isinstance(statement, StatementAssign):
            l, subexpr_result = self.bmm_expr(statement.rvalue)
            result = self.new_temp(statement.lvalue)
            #copy on assign
            opcode = "copy"
            args = [subexpr_result]
            return l + [TAC_line(opcode, args, result).format()]

            
    def bmm_expr(self,expression):
        """Takes an expression and returns a list of TAC statements"""
        #figure out bottom up numbering maybe add output of bmm expression,  so it gives list of instructions and 
        if isinstance(expression, ExpressionInt):
            opcode = "const"
            args = [expression.value] #what if two intergers same name?
            result = self.new_temp(f"{len(self.temps)}")
            return [TAC_line(opcode, args,result).format()], result
        elif isinstance(expression, ExpressionVar):
            # print(f"expression var: {expression.name}")
            return [], self.temps[expression.name]
        elif isinstance(expression, ExpressionOp) and len(expression.arguments) == 1:
            #unary operator
            opcode = self.operator_map[expression.operator]
            prev_lines, subexpr_result = self.bmm_expr(expression.arguments[0])
            result = self.new_temp(f"{len(self.temps)}")
            return prev_lines + [TAC_line(opcode, [subexpr_result], result).format()], result #figure out args from last one
        else:   #binary operator
            prev_lines = []
            opcode = self.operator_map[expression.operator]
            args = []
            for subexpr in expression.arguments: 
                line, subexpr_result = self.bmm_expr(subexpr)
                prev_lines += line
                args.append(subexpr_result)
            result = self.new_temp(f"{len(self.temps)}")
            return prev_lines + [TAC_line(opcode, args, result).format()], result #figure out args are last two

    def bmm(self):
        print(f"bmm")
        for item in self.tree.body:
            # print(f"line: {item}")
            self.body += self.bmm_stmt(item)
        # print(f"body: {self.body}")

class TAC_line:
    def __init__(self, opcode, args, result):
        self.opcode = opcode
        self.args = args
        self.result = result
    def format(self):
        return {"opcode": self.opcode, "args": self.args, "result": self.result}
