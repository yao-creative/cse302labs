import sys, argparse, json
from cfg import *
from typing import List

# ------------------------------------------------------------------------------#
# Basic Block Creator Class
# ------------------------------------------------------------------------------#

class CFG_creator:
    """ Creates Basic Block structure for CFG """
    # import jcc instr from Block class in cfg.py
    jccs = Block.jccs

    def __init__(self, func_name: str, tac_instr: List[dict], label: str) -> None:
        self.__func_name: str = func_name
        self.__tac_instr: List[dict] = tac_instr
        assert(tac_instr[-1]["opcode"] == "ret"), f"Last proc instr is not a ret in {func_name}"
        self.__label_counter: int = int(label)
        self.__new_labels: List[str] = list()
        self.__updated_tac_instr: List[dict] = self.__add_labels()
        self.__num_instr: int = len(self.__updated_tac_instr)
        self.__blocks: List[Block] = self.__block_inference()

    def __create_new_label(self) -> str:
        """ Create and return a new label """
        label = f"{self.__label_counter}"
        self.__label_counter += 1
        return label

    def __create_label_instr(self, name: str) -> dict:
        """ Create and returns a label instr for the proc """
        label_name = f".{self.__func_name}.L{name}"
        self.__new_labels.append(label_name)
        return {"opcode": "label",
                "args": [label_name],
                "result": None}

    def __add_labels(self) -> List[dict]:
        """ Divide proc code into basic blocks by adding labels """
        new_tac_instr: List = []
        # add entry label
        new_tac_instr.append(self.__create_label_instr("entry"))
        
        # parse tac instr to add lable after each jcc
        for index, instr in enumerate(self.__tac_instr):
            new_tac_instr.append(instr)
            if instr["opcode"] in self.jccs:
                # if the next instruction is not already a label then add one
                if self.__tac_instr[index+1]["opcode"] != "label":
                    new_tac_instr.append(self.__create_label_instr(self.__create_new_label()))

        return new_tac_instr

    def __block_inference(self) -> List[Block]:
        """ Creates Blocks from the updated tac_instr """
        current_block_instr = []
        blocks: List[Block] = []

        for index, instr in enumerate(self.__updated_tac_instr):
            # print(index)      # DEBUG
            # print(instr)      # DEBUG
            
            # append the first label instr and assert it is a label
            if not len(current_block_instr):
                assert(instr["opcode"] == "label"), f'First instruction not a label {instr}'

            # Create a block until a ret instr
            if instr["opcode"] == "ret":
                current_block_instr.append(instr)
                blocks.append(Block(current_block_instr))
                # print(current_block_instr)
                current_block_instr = []
                continue

            # end a block if next instr is label
            if self.__updated_tac_instr[index+1]["opcode"] == "label":
                current_block_instr.append(instr)
                blocks.append(Block(current_block_instr))
                # print(current_block_instr)
                current_block_instr = []
                continue

            else: current_block_instr.append(instr)

        # add jmp instr to all blocks
        for index, block in enumerate(blocks):
            # skip for first block
            if not index: continue
            # add jmp to curr block in prev block if not a jmp
            if blocks[index-1].last_instr_opcode() != "jmp":
                blocks[index-1].add_jmp(block.get_block_label())

        # assert all blocks end with jmp
        for block in blocks:
            # print(block.instructions())
            assert(block.last_instr_opcode() in ["jmp", "ret"]), \
                f'Block does not end with jmp or ret instr: {instr}'

        return blocks

    def return_blocks(self) -> List[Block]:
        """ Returns the list of blocks """
        return self.__blocks

# ------------------------------------------------------------------------------#
# Main function
# ------------------------------------------------------------------------------#

def get_serialized_tac(tac_instr: List[dict]) -> List[dict]:
    """ Creates the CFG for given tac instr """
    serialized_tac = []
    for decl in tac_instr:
        if "proc" in decl:
            # get the final prev label counter and 
            if len(decl["labels"]):
                label = int(decl["labels"][-1][3:])+1
            else:
                label = 0
            assert decl["proc"][0] == '@'
            basic_blocks = CFG_creator(decl["proc"][1:], decl["body"], label).return_blocks()
            cfg = CFG(basic_blocks, decl["proc"][1:])
            cfg.optimization()
            serialized_tac.append(cfg.serialized_tac())

    return serialized_tac

def write_serial_tac(filename: str, serialized_tac: List[dict]) -> None:
    """ Wrties the serialized tac to a json file """
    sname = filename + ".serial.json"
    with open(sname, "w") as fp:
        json.dump(serialized_tac, fp, indent=3)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get file')
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    filename = args.filename[0]     # get the filename
    assert(filename[-5:] == ".json"), f"Wrong format for input file {filename}"

    with open(filename, 'r') as fp: # save the file
        tac_instr = json.load(fp)

    serial_tac = get_serialized_tac(tac_instr)
    write_serial_tac(filename[:-5], serial_tac)