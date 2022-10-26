import sys, argparse
import cfg
from typing import List


# ------------------------------------------------------------------------------#
# Basic Block Creator Class
# ------------------------------------------------------------------------------#

class Basic_Block_Creator:
    """ Creates Basic Block structure """
    
    jccs = ["jmp",
            "jz", "jnz", 
            "jl", "jle",
            "jnl", "jnle",]

    def __init__(self, func_name: str, tac_instr: List[str], label: str) -> None:
        self.__func_name: str = func_name
        self.__tac_instr: List[dict] = tac_instr
        self.__num_instr: int = len(self.__tac_instr)
        self.__label_counter: int = int(label)+1
        self.__updated_tac_instr: List[dict] = self.__add_labels()
        self.__new_labels: List[str] = []
        self.__blocks: List[Block] = self.__block_inference()

    def __create_new_label(self) -> str:
        """ Create and return a new label """
        label = f".{self.__func_name}.L{self.__label_counter}"
        self.__label_counter += 1
        return label

    def __create_label_instr(self, name: str) -> dict:
        """ Create and returns a label instr for the proc """
        label_name = f".{self.__func_name}.L{name}"
        self.__new_labels.append(label_name)
        return {"opcode": "label",
                "args": [label_name],
                "result": None}

    def __add_labels(self) -> List[str]:
        """ Divide soruce code into basic blocks from proc instrs by adding labels """
        new_tac_instr: List = []

        # add entry label
        new_tac_instr.append(self.__create_label_instr("entry"))
        
        # parse tac instr to add lable after each jcc
        for index, instr in enumerate(self.__tac_instr):
            if instr["opcode"] in self.jccs:
                if index < self.__num_instr:
                    # if the next instruction is not already a label then add one
                    if self.__tac_instr[index+1]["opcode"] != "label":
                        new_tac_instr.append(self.__create_label_instr(self.__create_new_label()))
                    else:
                        new_tac_instr.append(instr)

        # add exit label
        new_tac_instr.append(self.__create_label_instr("exit"))

        return new_tac_instr

    def __block_inference(self) -> List[Block]:
        """ Creates Blocks from the updated tac_instr """

        current_block_instr = []
        blocks: List[Block] = []

        for index, instr in enumerate(self.__updated_tac_instr):
            # append the first label instr and assert it is a label
            if not len(current_block_instr):
                assert(instr["opcode"] == "label"), f'First instruction not a label {instr}'
                current_block_instr.append(instr)
            
            # Create a block until a ret instr and assert last instr is ret
            elif index == self.__num_instr or instr["opcode"] == "ret":
                assert(instr["opcode"] == "ret"), f'Last instr not a ret {instr}'
                current_block_instr.append(instr)
                blocks.append(Block(current_block_instr))
                current_block_instr = []

            # end a block if next instr is label and assert curr instr is a jcc
            elif self.__updated_tac_instr[index+1]["opcode"] == "label":
                assert(instr["opcode"] in self.jccs), f'Block does not end with jcc instr: {instr}'
                current_block_instr.append(instr)
                blocks.append(Block(current_block_instr))
                current_block_instr = []

            else:
                current_block_instr.append(instr)

        # add jmp instr to all blocks
        for index, block in enumerate(blocks):
            # skip for first block
            if not index: continue
            # add jmp to curr block in prev block if not a jmp
            if blocks[index-1].last_instr() != "jmp":
                blocks[index-1].add_jmp(block.block_label())

        # assert all blocks end with jmp
        for block in blocks:
            assert(block.last_instr() == "jmp"), f'Block does not end with jmp instr: {instr}'

        return blocks

    def return_blocks(self) -> List[Block]:
        """ Returns the list of blocks """
        return self.__blocks


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

    basic_blocks = Basic_Block_Creator(tac_instr["proc"][1:], tac_instr["body"], label)
