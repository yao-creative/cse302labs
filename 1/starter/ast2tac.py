from re import search
import sys
import json

#can assume that all of the variable names are distinct
class Decl:
    pass
    # def __init__(self,position):
    #     self.position = position 
class DeclProc(Decl):
    def __init__(self,name, arguments,returntype,body):
        self.name = name
        self.arguments = arguments
        self.returntype = returntype
        self.body = body
    def __str__(self):
        return "proc(%s,%s,%s,%s)" % (self.name,self.arguments,self.returntype,self.body)
class Statement:
    pass
    # def __init__(self,position):
    #     self.position = position
class StatementVardecl(Statement):
    def __init__(self,name, t, init):
        self.name = name
        self.type = t
        self.init = init 
    def __str__(self):
        return "vardecl(%s,%s,%s)" % (self.name,self.type,self.init)
class StatementEval(Statement):
    """Actually are are prints"""
    def __init__(self,arguments):
        self.arguments = arguments
    def __str__(self):
        return "print({})".format(self.arguments)
class StatementAssign(Statement):
    def __init__(self, lvalue,rvalue): 
        self.lvalue = lvalue
        self.rvalue = rvalue
    def __str__(self):
        return "StatementAssign(%s,%s)" % (self.lvalue,self.rvalue)
class Expression:
    pass
    # def __init__(self, position):
    #     self.position = position
class ExpressionVar(Expression):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "ExpressionVar({})".format(self.name)
class ExpressionInt(Expression):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "ExpressionInt({})".format(self.value)
class ExpressionOp(Expression):
    def __init__(self, operator, arguments):
        """operator: string of the operator
        arguments: list of expressions"""
        self.operator = operator
        self.arguments = arguments
    def __str__(self):
        return "ExpressionOp(%s,%s)" % (self.operator,self.arguments)


def json_to_name(js_obj):
    return js_obj[1]['value']
def parse_type_from_str(string):
    print(f"string: {string}")
    return string[6:-1] # from after colon to before last >
def json_to_expr(js_obj):
    """Takes a json object and returns an expression"""
    constructor = js_obj[0]
    if constructor == "<decl:proc>":
        name = json_to_name(js_obj[1]['name'])
        arguments = js_obj[1]['arguments']
        returntype = js_obj[1]['returntype']
        body = [json_to_expr(obj) for obj in js_obj[1]['body']]
        return DeclProc(name, arguments,returntype,body)
    if constructor == "<statement:vardecl>":
        name = json_to_name(js_obj[1]['name'])
        t = parse_type_from_str(js_obj[1]['type'][0])
        init = js_obj[1]['init'][1]["value"]
        return StatementVardecl(name, t,init)
    if constructor == "<statement:assign>":
        lvalue_name =json_to_name(js_obj[1]["lvalue"][1]["name"])
        lvalue  = ExpressionVar(lvalue_name)
        rvalue = json_to_expr(js_obj[1]["rvalue"])
        return StatementAssign(lvalue, rvalue)
    if constructor == "<statement:eval>": #all are prints
        return StatementEval(json_to_expr(js_obj[1]["expression"][1]["arguments"][0]))
    if constructor == "<expression:var>":
        return ExpressionVar(json_to_name(js_obj[1]['name']))
    if constructor == "<expression:int>":
        return ExpressionInt(js_obj[1]['value'])
    if constructor == "<expression:uniop>":
        operator = json_to_name(js_obj[1]['operator'])
        argument = json_to_expr(js_obj[1]['argument']) # recursive call
        return ExpressionOp(operator, [argument]) # TODO: raise error if not unary
    if constructor == "<expression:binop>":
        operator = json_to_name(js_obj[1]['operator'])
        left = json_to_expr(js_obj[1]['left']) # recursive call
        right = json_to_expr(js_obj[1]['right'])
        return ExpressionOp(operator,[left,right]) #TODO: raise error if not binary

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
            print(F"created new temp: {self.temps[key]}")
        else:
            print(F"temp already exists: {self.temps[key]}")
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
            opcode = "const"
            args = [statement.init] #initialization value of declaration
            result = self.new_temp(statement.name) #use the name of the variable as the key
            return [TAC_line(opcode, args, result).format()]
        elif isinstance(statement, StatementEval):
            temp_to_print = self.new_temp(f"{len(self.temps)}")
            #this is guaranteed unique since it is an integer and length keeps growing.
            prev_lines = self.tmm_expr(statement.arguments, temp_to_print)
            opcode = "print"
            result = None
            return prev_lines + [TAC_line(opcode, [temp_to_print], result).format()]
        elif isinstance(statement, StatementAssign):
            if self.search(statement.lvalue.name):
                result = self.temps[statement.lvalue.name]
            else:
                result = self.new_temp(statement.lvalue.name)
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
            self.body += self.tmm_stmt(item)
        print(f"body: {self.body}")
        
    #___________________________________________________________
    #BMM
    #___________________________________________________________
    def bmm_stmt(self,statement):
        """Takes a statement and returns a list of TAC statements"""
        if isinstance(statement, StatementVardecl):
            opcode = "const"
            args = [statement.init] #initialization value of declaration
            result = self.new_temp(statement.name) #use the name of the variable as the key
            return [TAC_line(opcode, args, result).format()]
        elif isinstance(statement, StatementEval):
            #this is guaranteed unique since it is an integer and length keeps growing.
            prev_lines,temp_to_print = self.bmm_expr(statement.arguments)
            opcode = "print"
            result = None
            return prev_lines + [TAC_line(opcode, [temp_to_print], result).format()]
        elif isinstance(statement, StatementAssign):
            print(f"expression assign")
            l, subexpr_result = self.bmm_expr(statement.rvalue)
            if self.search(statement.lvalue.name):
                result = self.temps[statement.lvalue.name]
            else:
                result = self.new_temp(statement.lvalue.name)
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
            print(f"expression var: {expression.name}")
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
            print(f"line: {item}")
            self.body += self.bmm_stmt(item)
        print(f"body: {self.body}")

class TAC_line:
    def __init__(self, opcode, args, result):
        self.opcode = opcode
        self.args = args
        self.result = result
    def format(self):
        return {"opcode": self.opcode, "args": self.args, "result": self.result}



if __name__ == "__main__":
    infile = sys.argv[1]
    with open(infile, 'r') as fp:
        js_obj = json.load(fp)
        js_obj = js_obj["ast"][0]

    tree =json_to_expr(js_obj)
    mm = sys.argv[2]
    TAC_proc(tree, mm).save(sys.argv[3])
    
#TMM
#---------------------------------------------------