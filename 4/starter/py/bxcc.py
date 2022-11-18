import sys, argparse
from typing import List

import ast2tac
import bx2front
import tac_cfopt
import tac2x64

def main(args: list) -> None:
    """ Main function to convert source code to asm """
    
    filename = args.filename[0]     # get the filename
    
    # convert tac to x64 directly
    if args.compiletac:
        if not filename.endswith('.tac.json'):
            print(f'File {filename} is not a tac json file')
            sys.exit(1)
        else:
            tac2x64.compile_tac(filename)
            sys.exit(0)

    # confirm that the file is bx file
    if not filename.endswith('.bx'):
        print(f'File {filename} is not a bx file')
        sys.exit(1)

    # run the bx2front.py file and get the ast
    ast = bx2front.get_ast(filename)
    
    # run ast2tac to get tac list
    tac_instr: List[dict] = ast2tac.ast_to_tac(ast)
    if args.keeptac:    # write the tac file
        ast2tac.write_tacfile(filename, tac_instr)
    # stop if only tac conversion requested
    if args.stoptac:
        sys.exit(0)

    # if CFG optimizations not requested then create asm and return
    if args.nocfg:
        tac2x64.convert_instr_to_asm(filename[:-3], tac_instr)
        sys.exit(0)

    # Do CFG optimizations
    serial_tac = tac_cfopt.get_serialized_tac(tac_instr)
    # stop if only CFG requested and write serialized tac
    tac_cfopt.write_serial_tac(filename[:-3], serial_tac)
    if args.stopcfg:
        sys.exit(0)
    
    # generate .s and .exe files
    tac2x64.convert_instr_to_asm(filename[:-3], serial_tac)

if __name__=="__main__":

    parse = argparse.ArgumentParser(description='BX-X64 compiler')
    parse.add_argument('--keep-tac', dest='keeptac', action='store_true', default=False,
                        help='Keep tac intermediary')
    parse.add_argument('--stop-tac', dest='stoptac', action='store_true', default=False,
                        help='Stop after tac generation')
    parse.add_argument('--compile-tac', dest='compiletac', action='store_true', default=False,
                        help='Compile from tac to x64')
    parse.add_argument('--stop-cfg', dest='stopcfg', action='store_true', default=False,
                        help='Perform CFG optimization and stop')
    parse.add_argument('--no-cfg', dest='nocfg', action='store_true', default=False,
                        help='Do not perform CFG optimization')
    parse.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parse.parse_args(sys.argv[1:])

    main(args)