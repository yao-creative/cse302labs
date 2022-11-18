from lib2to3.pgen2.parse import ParseError
import ply.yacc as yacc
from bxast import *
from scanner import tokens
import sys
import scanner
import ply.lex as lex

"""
Authors: Yi Yao Tan 
         Vrushank Agrawal
"""

__unop_dict = {
    '!': "not",
    '-': "opposite",
    '~': "bitwise-negation"
}

__binop_dict = {
                '+': "addition",
                '-': "substraction",
                '*': "multiplication",
                '/': "division",
                '%': "modulus",
                '&': "bitwise-and",
                '|': "bitwise-or",
                '^': "bitwise-xor",
                '<<': "logical-shift-left",
                '>>': "logical-shift-right",
                '==': "cmpe",
                '!=': "cmpne",
                '<': "cmpl",
                '>': "cmpg",
                '<=': "cmple",
                '>=': "cmpge",
                '&&': "logical-and",
                '||': "logical-or",
}

lexer = lex.lex(module=scanner)
previous_functions = []
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left','BITWISE_OR'),
    ('left','BITWISE_XOR'),
    ('left','BITWISE_AND'),
    ('nonassoc', 'CMPE', 'CMPNE'),
    ('nonassoc', 'CMPL', 'CMPLE', 'CMPG','CMPGE'),
    ('left','LOGICAL_SHIFT_LEFT', 'LOGICAL_SHIFT_RIGHT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'PERCENT'),
    ('right', 'UMINUS', 'NOT'),
    ('right', 'BITWISE_NEGATION'),
) 

def p_program(p):
    """program : declstar"""
    # print(f"entered program p[1]: {p[1]}")
    p[0] = Prog([p.lineno(0), p.lexpos(0)],p[1])
    # print(f"program: {p[0]}")
    
def p_declstar(p):
    """declstar : 
                | declstar decl"""           
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])
    # print(f"declstar: {p[0]}")

def p_decl(p):
    """decl : vardecl
            | procdecl"""
    # print(f"decl: {p[1]}")
    p[0] = p[1]
          
def p_procdecl(p):
    """procdecl : DEF IDENT LPAREN paramstar RPAREN type_optional block"""
    p[0]: DeclProc = DeclProc([p.lineno(0), p.lexpos(0)], p[2], p[4], p[6], p[7])
    
def p_type_optional(p):
    """type_optional : 
                       | COLON BOOL
                       | COLON INT"""
    if len(p) == 1:
        p[0] = BX_TYPE.VOID
    else:
        p[0] = BX_TYPE.INT if p[2] == "int" else BX_TYPE.BOOL
        
def p_type(p):
    """type : INT
            | BOOL"""
    p[0] = BX_TYPE.INT if p[1] == "int" else BX_TYPE.BOOL    
      
def p_paramstar(p):
    """paramstar : 
                 | param
                 | param COMMA paramstar"""
    # print(f"entered paramstar")
    if len(p) == 1:
        p[0] = []
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[3]
    # print(f"paramstar: {p[0]}")

def p_param(p):
    """param : identstar COLON type"""
    lp = ListParams([], p[3])
    # print(f"identstar p[2]: {p[2]}")
    lp.add_multi_param(p[1])
    p[0] = lp.return_params_list()

def p_identstar(p):
    """identstar : IDENT
                 | identstar COMMA IDENT"""
    if len(p) == 2:
        p[0] = [([p.lineno(0), p.lexpos(0)], p[1])]
    else:
        p[0] = p[1]
        p[0].append(([p.lineno(0), p.lexpos(0)], p[3]))
        
def p_statementstar(p):
    """statementstar :
                     | statementstar statement"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        if isinstance(p[2], list):
            p[0].extend(p[2])
        else:
            p[0].append(p[2])
        
def p_statement(p):
    """statement : vardecl
                 | eval
                 | assign
                 | block
                 | ifelse
                 | while
                 | jump
                 | return
                 """
    p[0] = p[1]
    
def p_eval(p):
    """eval : expression SEMICOLON"""
    p[0] = StatementEval([p.lineno(0), p.lexpos(0)],p[1])

def p_block(p):
    """block : LBRACE statementstar RBRACE"""
    p[0] = StatementBlock([p.lineno(0), p.lexpos(0)],p[2])

def p_assign(p):
    """assign : IDENT EQUALS expression SEMICOLON"""
    expr_var = ExpressionVar([p.lineno(0), p.lexpos(0)], p[1])
    p[0] = StatementAssign([p.lineno(0), p.lexpos(0)], expr_var, p[3])

def p_ifelse(p):
    """ifelse : IF LPAREN expression RPAREN block ifrest"""
    p[0] = StatementIfElse([p.lineno(0), p.lexpos(0)],p[3],p[5],p[6])

def p_ifrest(p):
    """ifrest : 
              | ELSE block
              | ELSE ifelse"""
    if len(p) == 1:
        p[0] = None
    elif len(p) == 3:
        p[0] = p[2]
    else:
        raise ParseError("Too many else statements")

def p_while(p):
    """while : WHILE LPAREN expression RPAREN block"""
    p[0] = StatementWhile([p.lineno(0), p.lexpos(0)],p[3],p[5])

def p_jump(p):
    """jump : BREAK SEMICOLON
            | CONTINUE SEMICOLON"""
    p[0] = StatementJump([p.lineno(0), p.lexpos(0)],p[1])

def p_return(p):
    """return : RETURN SEMICOLON
              | RETURN expression SEMICOLON"""
    if len(p) == 3:
        p[0] = StatementReturn([p.lineno(0), p.lexpos(0)],None)
    else:
        p[0] = StatementReturn([p.lineno(0), p.lexpos(0)],p[2])

def p_vardecl(p):
    """vardecl : VAR varinits COLON type SEMICOLON"""
    # print(f"variable declaration of type {p[4]}")
    listvardecl = ListVarDecl([], p[4])
    vars = p[2]
    # TODO smth wrong with global vars passing here
    # check examples/main_test.bx
    listvardecl.add_multi_var(vars)
    p[0] = listvardecl.return_vardecl_list()
    # print(f"vardecl: {p[0]}")
    
def p_varinits(p):
    """varinits : IDENT EQUALS expression varinitstar"""
    p[0] =  [([p.lineno(0), p.lexpos(0)], p[1], p[3])] + p[4]

def p_varinitstar(p):
    """varinitstar : 
                   | varinitstar COMMA IDENT EQUALS expression"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(([p.lineno(0), p.lexpos(0)], p[3], p[5]))
        
def p_expression(p):
    """expression : IDENT
                  | NUMBER
                  | TRUE
                  | FALSE
                  | LPAREN expression RPAREN
                  | expression binop expression
                  | MINUS expression %prec UMINUS
                  | NOT expression
                  | BITWISE_NEGATION expression
                  | IDENT LPAREN expressionstar RPAREN
    """
    if len(p) == 2:
        if p[1] == "true":
            p[0] = ExpressionBool([p.lineno(0), p.lexpos(0)], True)
        elif p[1] == "false":
            p[0] = ExpressionBool([p.lineno(0), p.lexpos(0)], False)
        elif isinstance(p[1], int):
            p[0] = ExpressionInt([p.lineno(0), p.lexpos(0)], p[1])
        elif isinstance(p[1], str):
            p[0] = ExpressionVar([p.lineno(0), p.lexpos(0)], p[1])
        else:
            raise SyntaxError("Invalid expression at line: " + str(p.lineno(0)))

    elif len(p) == 3:
        if p[1] not in __unop_dict:
            raise SyntaxError("Invalid unary operator at line: " + str(p.lineno(0)))
        op = __unop_dict[p[1]]
        p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)], op, [p[2]])

    elif len(p) == 4: 
        if p[1] == "(":
            p[0] = p[2]
        else:
            if p[2] not in __binop_dict:
                raise SyntaxError("Invalid binary operator at line: " + str(p.lineno(0)))
            op = __binop_dict.get(p[2])
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)], op, [p[1], p[3]])
            
    elif len(p) == 5: # function call
        params = p[3]
        p[0] = ExpressionProcCall([p.lineno(0), p.lexpos(0)], p[1], params)
        
    else:
        raise ParseError("Invalid expression with too many arguments at line: " + str(p.lineno(0)))
    
def p_expressionstar(p):
    """expressionstar : 
                      | expression 
                      | expressionstar COMMA expression"""
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])
        
def p_binop(p):
    """binop : PLUS         
             | MINUS        
             | MULTIPLY     
             | DIVIDE       
             | PERCENT      
             | BITWISE_AND  
             | BITWISE_OR   
             | BITWISE_XOR  
             | LOGICAL_SHIFT_LEFT
             | LOGICAL_SHIFT_RIGHT
             | CMPE         
             | CMPNE        
             | CMPL         
             | CMPLE        
             | CMPG         
             | CMPGE        
             | AND          
             | OR           """
    p[0] = p[1]
    
def p_error(p):
    if p:
        print(f"error: {p}")
        # print(f"Syntax error: at token at line: {p.lineno}")
        # Just discard the token and tell the parser it's okay.
    else:
        print(f"Syntax error: at EOF")
    sys.exit(1)

parser = yacc.yacc()

def run_parser(filename):
    """Parse a file and return the AST"""
    with open(filename) as f:
        data = f.read()

    result = parser.parse(data, lexer=lexer,tracking=True)
    # print(result)
    return result 

if __name__ == "__main__":
    res = run_parser(sys.argv[1])
