from typing import List

# ------------------------------------------------------------------------------#
# Block Class
# ------------------------------------------------------------------------------#

class Block:
    """ Class for every block in TAC instr """
    def __init__(self, instr: List[dict]) -> None:
        self.__instr: List[dict] = instr

    def block_label(self) -> str:
        """ Returns the name of the block's label """
        return self.__instr[0]["args"]

    def add_jmp(self, label: str) -> None:
        """ Adds a jmp instr to the end of block """
        self.__instr.append({"opcode": "jmp",
                             "args": [label],
                             "result": None})

    def last_instr(self) -> str:
        """ Returns the opcode of the last instr """
        return self.__instr[-1]["opcode"]

# ------------------------------------------------------------------------------#
# CFG Class
# ------------------------------------------------------------------------------#

class CFG:

    def __init__(self, blocks: List[Block]) -> None:
        self.__blocks: List[Block] = blocks

    def __serialize(self) -> None:
        """ Serialisation from CFG to TAC """
        
    


