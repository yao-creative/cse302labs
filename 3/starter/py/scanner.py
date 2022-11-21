import ply.lex as lex
import argparse
import sys

#words 
reserved = {
    "main" : "MAIN",
    "while": "WHILE",
    "print": "PRINT",
    "def" : "DEF",
    "int" : "INT",
    "var" : "VAR",
    "if" : "IF",
    "else": "ELSE",
    "while": "WHILE",
    "true": "TRUE",
    "false": "FALSE",
    "break": "BREAK",
    "continue": "CONTINUE"
}

#Symbols
#check to use NEGATIVE == UNARY MINUS
tokens = ("PLUS", "MINUS", "SEMICOLON", "COLON", "LPAREN", "RPAREN", "IDENT", "NUMBER", 
        "LBRACE", "RBRACE", "EQUALS", "MULTIPLY", "DIVIDE",
         "PERCENT", "BITWISE_AND", "BITWISE_OR", "BITWISE_XOR",
         "BITWISE_NEGATION", "LOGICAL_SHIFT_LEFT", "LOGICAL_SHIFT_RIGHT",
         "CMPE", "CMPNE", "CMPL", "CMPLE", "CMPG", "CMPGE", "AND", "OR", "NOT") + tuple(reserved.values())

#Non identifiers and numbers:

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_PERCENT = r'%'

t_EQUALS = r'='
t_SEMICOLON = r';'
t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_BITWISE_AND = r'&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\^'
t_BITWISE_NEGATION = r'~'
t_LOGICAL_SHIFT_LEFT = r'<<'
t_LOGICAL_SHIFT_RIGHT = r'>>'

t_CMPE = r'=='
t_CMPNE = r'!='
t_CMPL = r'<'
t_CMPLE = r'<='
t_CMPG = r'>'
t_CMPGE = r'>='

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'


def t_IDENT(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore_COMMENT = r'//.*\n?'
t_ignore = ' \t'

def t_error(t):
    print(f"Lexing error: Illegal Character '{t.value[0]}' on line {t.lexer.lineno} ")
    t.lexer.skip(1) 

def t_newline(t):
    r'\n'
    t.lexer.lineno +=1


    
if __name__ == "__main__":
    
    # parser = argparse.ArgumentParser(description= "Lex files")
    # parser.add_argument("--")
    lexer = lex.lex()
    file_to_lex = sys.argv[1]
    with open(file_to_lex, "r") as infile:
        for line in infile:
            lexer.input(line)
            for token in lexer:
                print(token)