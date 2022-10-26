import sched
from typing import List, Set

# ------------------------------------------------------------------------------#
# Block Class
# ------------------------------------------------------------------------------#

class Block:
    """ Class for every block in TAC instr """

    jccs = ["jmp",
            "jz", "jnz", 
            "jl", "jle",
            "jnl", "jnle",]

    def __init__(self, instr: List[dict]) -> None:
        self.__instr: List[dict] = instr
        self.__label_dest: Set[str] = set()
        self.allate_block_label_dests()

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

    def allate_block_label_dests(self) -> None:
        """ Returns all label destinations for jcc instr in the block """
        dest = set()
        for instr in self.__instr:
            if instr["opcode"] in self.jccs:
                dest.append(instr["args"][-1])
        self.__label_dest = dest

    def all_dests(self) -> Set[str]:
        """ Returns all jcc label dests for current block """
        self.allate_block_label_dests()
        return self.__label_dest


# ------------------------------------------------------------------------------#
# CFG Class
# ------------------------------------------------------------------------------#

class CFG:
    """ Creates CFG representation for internal use """
    def __init__(self, blocks: List[Block]) -> None:
        self.__blocks: List[Block] = blocks
        self.__entry_block: Block = self.__blocks[0]
        self.__edges: dict = dict()
        self.__update_block_edges()
        # blocks needed to be called by labels for serialization
        self.__blocks_by_labels: dict = {block.block_label(): block for block in self.__blocks}

    def __update_block_edges(self) -> dict:
        """ Updates all edges btw cfg blocks """
        edges = {}
        for block in self.__blocks:
            edges[block.block_label()] = block.all_dests()
        self.__edges = edges

    # ---------------------------------------------------------------------------#
    # CFG Operations
    # ---------------------------------------------------------------------------#





    # ---------------------------------------------------------------------------#
    # Serialization
    # ---------------------------------------------------------------------------#

    def __serialize(self) -> List[Block]:
        """ Serialisation from CFG to TAC """
        curr_block: Block = self.__entry_block 
        scheduled: List[Block] = list()
        next_labels = curr_block.all_dests()
        successors: Set[str] = set()
        
        while curr_block is not None:
            scheduled.append(curr_block)
            for label in next_labels:
                successors.add(self.__blocks_by_labels(label))
            if successors:
                curr_block = successors.pop()
                next_labels = curr_block.all_dests()
            else:
                curr_block = None

        return scheduled
