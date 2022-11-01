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
    """program : DEF MAIN LPAREN RPAREN block"""
    previous_functions.append(p[2])
    if len(previous_functions) > 1:
        raise SyntaxError("Too many main functions")
    if p[2] != "main":
        raise SyntaxError("Function is not main!")
    p[0] = DeclProc([p.lineno(0), p.lexpos(0)], p[2], [], None, p[5], previous_functions)

def p_block(p):
    """block : LBRACE statementstar RBRACE"""
    p[0] = StatementBlock([p.lineno(0), p.lexpos(0)],p[2])

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
                 | print
                 | block
                 | ifelse
                 | while
                 | jump
                 """
    p[0] = p[1]

def p_vardecl(p):
    """vardecl : VAR IDENT EQUALS expression COLON INT SEMICOLON"""
    p[0] = StatementVardecl([p.lineno(0), p.lexpos(0)],
                            ExpressionVar([p.lineno(0), p.lexpos(0)],p[2]),
                            "int",p[4])

def p_assign(p):
    """assign : IDENT EQUALS expression SEMICOLON"""
    p[0] = StatementAssign([p.lineno(0), p.lexpos(0)],
    ExpressionVar([p.lineno(0), p.lexpos(0)],p[1]),p[3])

def p_print(p):
    """print : PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = StatementPrint([p.lineno(0), p.lexpos(0)],p[3])
    
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

def p_expression(p):
    """expression : IDENT
                  | NUMBER
                  | TRUE
                  | FALSE
                  | LPAREN expression RPAREN
                  | expression PLUS         expression
                  | expression MINUS        expression
                  | expression MULTIPLY     expression
                  | expression DIVIDE       expression
                  | expression PERCENT      expression
                  | expression BITWISE_AND  expression
                  | expression BITWISE_OR   expression
                  | expression BITWISE_XOR  expression
                  | expression LOGICAL_SHIFT_LEFT expression
                  | expression LOGICAL_SHIFT_RIGHT expression
                  | expression CMPE         expression
                  | expression CMPNE        expression
                  | expression CMPL         expression
                  | expression CMPLE        expression
                  | expression CMPG         expression
                  | expression CMPGE        expression
                  | expression AND          expression
                  | expression OR           expression
                  | MINUS expression %prec UMINUS
                  | NOT expression
                  | BITWISE_NEGATION expression
    """
    if len(p) == 2:
        if p[1] == "true":
            p[0] = ExpressionBool([p.lineno(0), p.lexpos(0)], True)
        elif p[1] == "false":
            p[0] = ExpressionBool([p.lineno(0), p.lexpos(0)], False)
        elif isinstance(p[1], int):
            p[0] = ExpressionInt([p.lineno(0), p.lexpos(0)],p[1])
        elif isinstance(p[1], str):
            p[0] = ExpressionVar([p.lineno(0), p.lexpos(0)],p[1])
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
    else:
        raise ParseError("Invalid expression with too many arguments at line: " + str(p.lineno(0)))

def p_error(p):
    if p:
        print(f"Syntax error: at token at line: {p.lineno}")
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
    print(res)
    


    