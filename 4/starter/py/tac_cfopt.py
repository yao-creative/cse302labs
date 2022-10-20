import sys, argparse
from typing import List

class Block:

    def __init__(self) -> None:
        pass


class CFG_creator:

    jmps = ["jmp", "ret", 
            "jz", "jnz", 
            "jl", "jle",
            "jnl", "jnle",]

    def __init__(self, func_name: str, tac_instr: List[str], label: str) -> None:
        self.__func_name : str = func_name
        self.__tac_instr : List[str] = tac_instr
        self.__num_instr: int = len(self.__tac_instr)
        self.__label_counter: int = int(label)
        self.add_labels()
        self.__blocks: List[Block] = self.block_inference()

    def add_labels(self) -> List[Block]:
        """ Construct basic blocks from proc instrs """
        if self.__tac_instr[0]["opcode"] != "label":
            entry_label = {"opcode": "label",
                           "args": [f".{self.__func_name}.Lentry"],
                           "result": None}
            self.__tac_instr = [entry_label] + [self.__tac_instr]
        
        for index, instr in enumerate(self.__tac_instr):
            if instr["opcode"] in self.jmps:
                if index < self.__num_instr:
                    if self.__tac_instr[index+1]["opcode"] != "label":
                        pass


# ------------------------------------------------------------------------------#
# Main function
# ------------------------------------------------------------------------------#


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get method for conversion and filetype.')
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename

    with open(filename, 'r') as fp:         # save the file
        tac_instr = fp.read()

    if len(tac_instr["labels"]):
        label = tac_instr["labels"][-1][3:]

    cfg = CFG_creator(tac_instr["proc"][1:], tac_instr["body"], label)
