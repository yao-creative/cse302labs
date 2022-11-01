from my_parser import parse_file
from ast2tac import TAC_proc
import sys
from tac2x64 import compile_tac

def main():
    if len(sys.argv) != 4:
        print("Usage: bx2asm.py <input-.bx-file> <--tmm||--bmm> <output-.tac.json-file>")
        sys.exit(1)
    # print(f"parsing")
    ast = parse_file(sys.argv[1])
    print(f"file: {sys.argv[1]}")
    # print(f"ast: {ast}")
    ast.syntax_check()

    tac = TAC_proc(ast,sys.argv[2]).save(sys.argv[3])
    print(f"saved")
    compile_tac(sys.argv[3])

if __name__ == "__main__":
    main()