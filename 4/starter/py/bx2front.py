import argparse
import sys
from bxast import Prog
from my_parser import run_parser

def get_ast(fname) -> Prog:
    ast: Prog = run_parser(fname)
    ast.global_type_check()
    print("global type_check done")
    ast.type_check()
    print("type_check done")
    return ast

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get method for conversion and filetype.')
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename

    ast = get_ast(filename)  # get the ast