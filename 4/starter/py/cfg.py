from typing import List, Set, Tuple, Union

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
        self.__label_dest: Set[str] = set()
        self.__succ: Union[str, False] = list(self.__label_dest[0])[0] if len(self.__label_dest) == 1 else False
        self.__successor_labels()

    def __hash__(self) -> int:
        """ Used for dict storing of pred values in CFG class """
        return hash(self.__label_dest)

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

    def __successor_labels(self) -> None:
        """ Returns all label destinations for jcc instr in the block """
        dest = set()
        for instr in self.__instrs:
            if instr["opcode"] in self.jccs:
                dest.append(instr["args"][-1])
        self.__label_dest = dest

    def successors(self) -> Set[str]:
        """ Returns all jcc label dests for current block """
        self.__successor_labels()
        return self.__label_dest

    def block_label(self) -> str:
        """ Returns the name of the block's label """
        return self.__instrs[0]["args"]


# ------------------------------------------------------------------------------#
# CFG Class
# ------------------------------------------------------------------------------#

class CFG:
    """ Creates CFG representation for internal use """

    def __init__(self, blocks: List[Block]) -> None:
        self.__blocks: List[Block] = blocks
        self.__entry_block: Block = self.__blocks[0]
        self.__edges: dict = dict()
        self.__update_next()
        # blocks needed to be called by labels for serialization
        self.__blocks_by_labels: dict = {block.block_label(): block for block in self.__blocks}
        self.__predecessors: dict = {block.block_label(): [] for block in self.__blocks}

    # ---------------------------------------------------------------------------#
    # Helper functions

    def __update_next(self) -> None:
        """ Updates all edges in cfg blocks """
        edges = {}
        for block in self.__blocks:
            edges[block.block_label()] = block.successors()
        self.__edges = edges

    def __next(self, block: Block) -> List[Block]:
        """ Returns the successor blocks of the current block """
        succ_labels = self.__edges[block.block_label()]
        blocks = [self.__blocks_by_labels[lab] for lab in succ_labels]
        return blocks

    def __update_prev(self) -> None:
        """ Updates the predecessor graph """
        for block in self.__blocks:
            for label in block.successors():
                self.__predecessors[label] += block.block_label()

    def __prev(self, block: Block) -> List[Block]:
        """ Returns the predecessor blocks for the current block """
        pred_labels = self.__predecessors[block.block_label()]
        blocks = [self.__blocks_by_labels[lab] for lab in pred_labels]
        return blocks

    def __coalesce_blocks(self, block1: Block, block2: Block) -> Block:
        """ Coalesce and return the given blocks """
        block1.remove_last_jmp()
        block1.add_instrs(block2.instructions())
        return block1

    # ---------------------------------------------------------------------------#
    # CFG Operations

    def __uce(self) -> None:
        """ Unreachable Code Elimination """


    def __coalescing(self) -> None:
        """ Colaesce two blokcs if one succ and one pred """


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
                successors.add(self.__blocks_by_labels(label))
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