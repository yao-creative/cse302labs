import sys, json, argparse
import ast2tac
import tac2x64
from ast2tac import AST_to_TAC_Generator

if __name__=="__main__":

    parse = argparse.ArgumentParser(description='BX-X64 compiler')
    parse.add_argument('--keep-tac', dest='keeptac', action='store_true', default=False,
                        help='Keep tac intermediary')
    parse.add_argument('--stop-tac', dest='stoptac', action='store_true', default=False,
                        help='Stop after tac generation')
    parse.add_argument('--compile-tac', dest='compiletac', action='store_true', default=False,
                        help='Compile from tac to x64')
    parse.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parse.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename
    
    if args.compiletac:
        if not filename.endswith('.tac.json'):
            print(f'File {filename} is not a tac json file')
            sys.exit(1)
        else:
            tac2x64.compile_tac(filename)
            sys.exit(0)

    if not filename.endswith('.bx'):
        print(f'File {filename} is not a bx file')
        sys.exit(1)

    tac_: AST_to_TAC_Generator = ast2tac.source_to_tac(filename)
    tac_instr = tac_.tac_generator()
    if args.keeptac:
        ast2tac.write_tacfile(filename, tac_instr)
    
    if args.stoptac:
        sys.exit(0)
        
    tac2x64.convert_instr_to_asm(filename[:-3], tac_instr)