import ply.yacc as yacc
from bxast import *
from scanner import tokens
import sys
import scanner
import ply.lex as lex

lexer = lex.lex(module=scanner)
declared_ids =[]
previous_functions = []
precedence = (
    ('left','BITWISE_OR'),
    ('left','BITWISE_XOR'),
    ('left','BITWISE_AND'),
    ('left','LOGICAL_SHIFT_LEFT', 'LOGICAL_SHIFT_RIGHT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'PERCENT'),
    ('right', 'UMINUS'),
    ('right', 'BITWISE_NEGATION'),
) 
def p_program(p):
    """program : DEF MAIN LPAREN RPAREN LBRACE statementstar RBRACE"""
    previous_functions.append(p[2])
    if len(previous_functions) > 1:
        raise SyntaxError("Too many main functions")
    if p[2] != "main":
        raise SyntaxError("Function is not main!")
    p[0] = DeclProc([p.lineno(0), p.lexpos(0)], p[2], [], None, p[6], previous_functions)



def p_statementstar(p):
    """statementstar :
                     | statementstar statement"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])

def p_statement(p):
    """statement : vardecl
                 | assign
                 | print"""
    p[0] = p[1]

def p_vardecl(p):
    """vardecl : VAR IDENT EQUALS expression COLON INT SEMICOLON"""
    p[0] = StatementVardecl([p.lineno(0), p.lexpos(0)],p[2],"int",p[4],declared_ids)
    declared_ids.append(p[2])

def p_assign(p):
    """assign : IDENT EQUALS expression SEMICOLON"""
    p[0] = StatementAssign([p.lineno(0), p.lexpos(0)],p[1],p[3],declared_ids)

def p_print(p):
    """print : PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = StatementPrint([p.lineno(0), p.lexpos(0)],p[3])


def p_expression(p):
    """expression : expression PLUS expression
                | expression MINUS expression
                | expression MULTIPLY expression
                | expression DIVIDE expression
                | expression PERCENT expression
                | expression BITWISE_AND expression
                | expression BITWISE_OR expression
                | expression BITWISE_XOR expression
                | expression LOGICAL_SHIFT_LEFT expression
                | expression LOGICAL_SHIFT_RIGHT expression
                | LPAREN expression RPAREN
                | MINUS expression %prec UMINUS
                | BITWISE_NEGATION expression
                | NUMBER
                | IDENT"""
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = ExpressionInt([p.lineno(0), p.lexpos(0)],p[1])
        else:
            p[0] = ExpressionVar([p.lineno(0), p.lexpos(0)],p[1],declared_ids)
    elif len(p) == 3:
        if p[1] == '-':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"opposite",[p[2]])
        else: # p[1] == '~'
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"bitwise-negation",[p[2]])
    elif len(p) == 4:
        if p[2] == '+':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"addition",[p[1],p[3]])
        elif p[2] == '-':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"substraction",[p[1],p[3]])
        elif p[2] == '*':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"multiplication",[p[1],p[3]])
        elif p[2] == '/':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"division",[p[1],p[3]])
        elif p[2] == '%':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"modulus",[p[1],p[3]])
        elif p[2] == '&':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"bitwise-and",[p[1],p[3]])
        elif p[2] == '|':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"bitwise-or",[p[1],p[3]])
        elif p[2] == '^':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"bitwise-xor",[p[1],p[3]])
        elif p[2] == '<<':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"logical-shift-left",[p[1],p[3]])
        elif p[2] == '>>':
            p[0] = ExpressionOp([p.lineno(0), p.lexpos(0)],"logical-shift-right",[p[1],p[3]])
        else: # p[2] == '('
            p[0] = p[2] 


def p_error(p):
    if p:
        print(f"Syntax error: at token at line: {p.lineno}")
        # Just discard the token and tell the parser it's okay.

    else:
        print(f"Syntax error: at EOF")
    sys.exit(1)
parser = yacc.yacc()

def parse_file(filename):
    """Parse a file and return the AST"""
    with open(filename) as f:
        data = f.read()

    result = parser.parse(data, lexer=lexer,tracking=True)
    # print(result)
    return result 

if __name__ == "__main__":
    parse_file(sys.argv[1])


    