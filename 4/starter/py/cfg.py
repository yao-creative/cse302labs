from operator import imod
from typing import List, Set, Dict, Union

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
        self.__instrs: List[dict] = instr
        self.__successors: list = []
        self.__update_successors()
        self.__pred: list = []

    # ---------------------------------------------------------------------------#
    # Instr helpers

    def add_jmp(self, label: str) -> None:
        """ Adds a jmp instr to the end of block """
        self.__instrs.append({"opcode": "jmp",
                              "args": [label],
                              "result": None})

    def last_instr(self) -> str:
        """ Returns the opcode of the last instr """
        return self.__instrs[-1]["opcode"]

    def remove_last_jmp(self) -> None:
        """ Removes the last jmp instr of the block for coalescing """
        assert(self.__instrs[-1]["opcode"] == "jmp"), f"Last instr is not jmp in the block {self.__instrs[-1]}"
        self.__instrs = self.__instrs[:-1]

    def instructions(self) -> List[dict]:
        """ Returns all block instrs """
        return self.__instrs

    def add_instrs(self, instrs: List[dict]) -> None:
        """ Add instrs to the block for coalesce """
        self.__instrs += instrs

    # ---------------------------------------------------------------------------#
    # Label helpers

    def block_label(self) -> str:
        """ Returns the name of the block's label """
        return self.__instrs[0]["args"]

    def __update_successors(self) -> None:
        """ updates all successors for the block """
        dest = []
        for instr in self.__instrs:
            if instr["opcode"] in self.jccs:
                if instr["args"][-1] not in dest:
                    dest.append(instr["args"][-1])
        self.__successors = dest

    def set_pred(self, preds: list) -> str:
        """ Sets the predecessor for the curr block """
        self.__pred = preds

    def ret_successors(self) -> list:
        """ Returns all successors for current block """
        self.__update_successors()
        return self.__successors

    def ret_predecessors(self) -> list:
        """ Returns all predecessors for current block """
        return self.__pred

    def has_one_succ(self) -> bool:
        """ If block has one succ return True """
        return len(self.__successors) == 1

    def has_one_pred(self) -> bool:
        """ If blokc has one pred return True """
        return len(self.__pred) == 1

# ------------------------------------------------------------------------------#
# CFG Class
# ------------------------------------------------------------------------------#

class CFG:
    """ Creates CFG representation for internal use """

    def __init__(self, blocks: List[Block]) -> None:
        self.__blocks: List[Block] = blocks
        self.__num_blocks: int = len(self.__blocks)
        self.__entry_block: Block = self.__blocks[0]
        self.__successors: Dict[str, set] = dict()
        self.__update_next()
        self.__update_prev()
        self.__labels_to_blocks: Dict[str, Block] = {block.block_label(): block for block in self.__blocks}
        self.__predecessors: dict = {block.block_label(): [] for block in self.__blocks}

    # ---------------------------------------------------------------------------#
    # Helper functions

    def __update_next(self) -> None:
        """ Updates all edges in cfg blocks """
        edges = {}
        for block in self.__blocks:
            edges[block.block_label()] = block.successors()
        self.__successors = edges

    def __update_prev(self) -> None:
        """ Updates the predecessor graph {label: [label]}"""
        pred_graph = dict()
        for block in self.__blocks:
            for label in block.successors():
                pred_graph[label] += block.block_label()
        self.__predecessors = pred_graph
        for lab, preds in pred_graph.items():
            self.__labels_to_blocks[lab].set_pred(preds)

    def __next(self, label: str) -> List[str]:
        """ Returns the successor labels of the current label """
        self.__update_next()
        return self.__successors[label]

    def __prev(self, block: Block) -> List[Block]:
        """ Returns the predecessor blocks for the current block """
        pred_labels = self.__predecessors[block.block_label()]
        blocks = [self.__labels_to_blocks[lab] for lab in pred_labels]
        return blocks

    def __coalesce_blocks(self, block1: Block, block2: Block) -> Block:
        """ Coalesce and return the given blocks """
        block1.remove_last_jmp()
        block1.add_instrs(block2.instructions())
        return block1

    def __coalescable(self, block1: Block, block2: Block) -> bool:
        """ Checks if given blocks can be coalesced """
        if block1.has_one_succ() and block2.has_one_pred():
            if block1.ret_successors()[0] == block2.ret_predecessors()[0]:
                return True
        return False

    def __del_block(self, block: Block) -> None:
        """ Delete the given block """
        self.__blocks.remove(block)
        del self.__successors[block.block_label()]
        self.__update_next()
        self.__entry_block = self.__blocks[0]

    # ---------------------------------------------------------------------------#
    # CFG Operations

    def __uce(self) -> None:
        """ Unreachable Code Elimination """
        visited_blocks = {self.__entry_block.block_label()}
        to_visit = self.__entry_block.ret_successors()
        while len(to_visit) > 0:
            label = to_visit.pop()
            if label not in visited_blocks:
                visited_blocks.add(label)
                to_visit.extend(self.__next(label))

        to_delete = []
        for block in self.__blocks:
            if block.block_label() not in visited_blocks:
                to_delete.append(block)
        for block in to_delete:
            self.__del_block(block)

    def __coalescing(self) -> None:
        """ Colaesce two blokcs if one succ and one pred """
        self.__update_prev()
        index = 0
        while index < self.__num_blocks:
            block = self.__blocks[index]
            next_block = self.__blocks[index+1]
            if self.__coalescable(block, next_block):
                new_block = self.__coalesce_blocks(block, next_block)


    # ---------------------------------------------------------------------------#
    # Serialization

    def __serialize(self) -> List[Block]:
        """ Serialisation from CFG to TAC """
        curr_block: Block = self.__entry_block 
        scheduled: List[Block] = list()
        next_labels = curr_block.successors()
        successors: Set[str] = set()
        
        while curr_block is not None:
            scheduled.append(curr_block)
            for label in next_labels:
                successors.add(self.__labels_to_blocks(label))
            if successors:
                curr_block = successors.pop()
                next_labels = curr_block.successors()
            else:
                curr_block = None

        return scheduled

    def serialized_tac(self) -> List[dict]:
        """ Returns serialized TAC instr """
        blocks = self.__serialize()
        tac_instrs = []
        for block in blocks:
            tac_instrs += block.instructions()
        return tac_instrs