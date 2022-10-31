from typing import List, Set, Dict, Tuple

# ------------------------------------------------------------------------------#
# Block Class
# ------------------------------------------------------------------------------#

class Block:
    """ Class for every block in TAC instr """

    jccs = ["jmp",
            "jz", "jnz", 
            "jl", "jle",
            "jnl", "jnle",]

    __no_jmp_jccs = ["jz", "jnz", 
                   "jl", "jle",
                   "jnl", "jnle",]

    def __init__(self, instr: List[dict]) -> None:
        self.__instrs: List[dict] = instr
        self.__label: str = self.__instrs[0]["args"]
        self.__successors: List[str] = []
        self.__pred: List[str] = []
        self.__cond_jmps: List[Tuple[int, dict]] = list()
        self.update_successors()
        self.update_cond_jmps()

    # ---------------------------------------------------------------------------#
    # Instr helpers

    def add_jmp(self, label: str) -> None:
        """ Adds a jmp instr to the end of block """
        if len(self.__instrs) > 0:
            assert(self.__instrs[-1]["opcode"] != "jmp"), f"a jmp instr already exists {self.__instrs[-1]}"
        self.__instrs.append({"opcode": "jmp", "args": [label], "result": None})

    def last_instr_opcode(self) -> str:
        """ Returns the opcode of the last instr """
        assert(len(self.__instrs) > 0), f"There are no instr in: {self}"
        return self.__instrs[-1]["opcode"]

    def last_instr_label(self) -> str:
        """ Returns the dest label of the last jmp instr """
        assert(len(self.__instrs) > 0), f"There are no instr in: {self}"
        return self.__instrs[-1]["args"][-1]

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
    # jcc instr helpers

    def update_cond_jmps(self) -> List[Tuple[int, dict]]:
        """ Returns list of all cond jumps """
        cond_js = []
        for index, instr in enumerate(self.__instrs):
            if instr["opcode"] in self.__no_jmp_jccs:
                cond_js.append((index, instr))
        self.__cond_jmps = cond_js

    def get_cond_jmps(self) -> List[Tuple[int, dict]]:
        """ Returns cond jmps list with instr indexes """
        return self.__cond_jmps

    def jcc_with_temp(self, temp: str) -> List[Tuple[int, dict]]:
        """ Checks and returns all jcc instr with the temp """
        cond_jmps = self.get_cond_jmps()
        jccs_with_temp = []
        for index, instr in cond_jmps:
            assert(instr["opcode"] in self.jccs), f"Wrong instr in cond_jmps: {instr}"
            if instr["args"][0] == temp:
                return jccs_with_temp.append((index, instr))
        return jccs_with_temp

    def is_temp_modified(self, start_index: int, stop_index: int, temp: str) -> bool:
        """ Checks if the temp has been modified in the prev instr """
        assert(start_index <= stop_index), f"start_index cannot be greater than stop_index for temp: {temp}"
        assert(stop_index < len(self.__instrs)), f"stop_index cannot be greater than instrs len for temp: {temp}"
        for i in range(start_index, stop_index):
            if self.__instrs[i]["result"] == temp:
                return True 
        return False

    def del_after_cond_jmp(self, index: int) -> None:
        """ Removes all code after cond jmp """
        assert(index < len(self.__instrs)), f"index: {index} out of bounds for block instrs: {self.__instrs}"
        self.__instrs = self.__instrs[:index]
    
    def del_cond_jmp(self, index: int) -> None:
        """ Deletes the cond jmp at given index """
        assert(index < len(self.__instrs)), f"Instr index: {index} out of range for {self.__instrs}"
        if index == len(self.__instrs)-1:
            self.__instrs = self.__instrs[:index]
        else:
            self.__instrs = self.__instrs[:index] + self.__instrs[index+1:]

    # ---------------------------------------------------------------------------#
    # Label helpers

    def block_label(self) -> str:
        """ Returns the name of the block's label """
        return self.__label

    def update_successors(self) -> None:
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

    def successors(self) -> List[str]:
        """ Returns all successors for current block """
        self.update_successors()
        return self.__successors

    def predecessors(self) -> list:
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

    def __init__(self, blocks: List[Block], func_name: str) -> None:
        self.__proc_name: str = func_name
        self.__blocks: List[Block] = blocks
        self.__num_blocks: int = len(self.__blocks)
        self.__entry_block: Block = self.__blocks[0]
        self.__successors: Dict[str, List[str]] = dict()
        self.__labels_to_blocks: Dict[str, Block] = self.__label_to_block_mapper()
        self.__predecessors: Dict[str, List[str]] = dict()
        self.__deleted_labels: Set[str] = set()

    # ---------------------------------------------------------------------------#
    # Helper functions

    def __label_to_block_mapper(self) -> Dict[str, Block]:
        """ Creates a map for labels to their block """
        return {block.block_label(): block for block in self.__blocks}

    def __update_edges(self) -> None:
        """ Updates all edges in cfg blocks """
        edges = {}
        for block in self.__blocks:
            edges[block.block_label()] = block.successors()
        self.__successors = edges

    def __update_pred_edges(self) -> None:
        """ Updates the pred graph in the blocks """
        pred_graph = {block.block_label(): [] for block in self.__blocks}
        for block in self.__blocks:
            for label in block.successors():
                assert(label in pred_graph), f"unidentified block label {label}"
                pred_graph[label] += block.block_label()
        self.__predecessors = pred_graph

        # update pred list in every block
        for lab, preds in pred_graph.items():
            self.__labels_to_blocks[lab].set_pred(preds)

    def __next(self, label: str) -> List[str]:
        """ Returns the succ labels of the curr label """
        self.__update_edges()
        return self.__successors[label]

    def __prev(self, block: Block) -> List[Block]:
        """ Returns the predecessor blocks for the current block """
        self.__update_pred_edges()
        pred_labels = self.__predecessors[block.block_label()]
        return pred_labels

    def __coalesce_blocks(self, block1: Block, block2: Block) -> Block:
        """ Coalesce and return the first block """
        block1.remove_last_jmp()
        block1.add_instrs(block2.instructions())
        return block1

    def __coalescable(self, block1: Block, block2: Block) -> bool:
        """ Checks if given blocks are coalescable """
        if block1.has_one_succ() and block2.has_one_pred():
            if block1.last_instr_label() == "jmp":
                if block1.successors()[0] == block2.predecessors()[0]:
                    return True
        return False

    def __del_block(self, block: Block) -> None:
        """ Delete the given block because it has no pred """
        self.__blocks.remove(block)
        self.__num_blocks = len(self.__blocks)
        del self.__labels_to_blocks[block.block_label()]
        self.__update_edges()
        self.__entry_block = self.__blocks[0]

    def __thread(self, block1: Block, block2: Block) -> None:
        """ Threads two blocks """
        if len(block2.instructions()) == 1:
            if block2.last_instr_opcode() == "label" and block1.last_instr_opcode() == "label":
                if block1.last_instr_label() == block2.block_label():
                    block1.remove_last_jmp()
                    block1.add_jmp(block2.last_instr_label())

    __jcc_direct_implication = {"jz":["jz"], "jnz":["jnz"],
                    "jl":["jl", "jle", "jnz"], "jle":["jle"],
                    "jnl":["jnl"], "jnle":["jnle", "jnl", "jnz"],}

    __jcc_neg_implications = {"jz":["jl", "jnle", "jnz"], "jnz":["jz"],
                 "jl":["jnl", "jnle", "jz"], "jle":["jnle"],
                 "jnl":["jl"], "jnle":["jz", "jl", "jle"],}

    def __check_jcc(self, block: Block) -> None:
        """ Checks if block has removable cond jmp """
        jcc_instrs = block.get_cond_jmps()
        for index, instr in jcc_instrs:
            dest_block = self.__labels_to_blocks[instr["args"][-1]]
            temp = instr["args"][0]
            jcc = instr["opcode"]
            
            # check if dest block has only one pred
            if self.__prev(dest_block) != dest_block.block_label():
                break
            # check if any jcc uses the temp for comparison
            jccs_with_temp = dest_block.jcc_with_temp(temp)
            if jccs_with_temp == []: 
                break
            
            # need to check if temp is modified in a range of instr
            prev_index = 0
            # need to delete neg jcc instrs that will always be False
            instr_index_to_delete = []
            
            for dest_index, dest_instr in jccs_with_temp:
                # if the temp has modified befor jcc instr then break
                if dest_block.is_temp_modified(prev_index, dest_index, temp):
                    break
                
                # if jcc instr is a direct implication then it will be True
                if dest_instr["opcode"] in self.__jcc_direct_implication[jcc]:
                    dest_lab = dest_instr["args"][-1]
                    block.del_after_cond_jmp(dest_index)
                    block.add_jmp(dest_lab)
                    break
                
                # if jcc instr is a direct neg implication then it will be False
                if dest_instr["opcode"] in self.__jcc_neg_implications[jcc]:
                    instr_index_to_delete.append(dest_index)
                
                prev_index = dest_index+1

            # delete False cond jmps in reverse
            for index in instr_index_to_delete[::-1]:
                dest_block.del_cond_jmp(index)

            # update cond jmps list in the block
            dest_block.update_cond_jmps()

    # ---------------------------------------------------------------------------#
    # CFG Operations

    def uce(self) -> None:
        """ Unreachable Code Elimination """
        self.__update_pred_edges()
        self.__update_edges()
        visited_blocks = {self.__entry_block.block_label()}
        to_visit = self.__entry_block.successors()
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
            self.__deleted_labels.add(block.block_label().replace(".main", "%"))

    def coalesce(self) -> None:
        """ Coalesce two blocks if one succ and one pred """
        self.__update_pred_edges()
        
        # we go bottom-up because if two blocks can be coalesced then 
        # the bottom block is shifted to the one above. This is faster to
        # implement than top-bottom where we'll need to run nested for loop 
        index = self.__num_blocks-1
        while index > 1:
            block = self.__blocks[index]
            prev_block = self.__blocks[index-1]
            if self.__coalescable(prev_block, block):
                # update the prev_block
                # the current block will be deleted in UCE
                self.__blocks[index-1] = self.__coalesce_blocks(block, prev_block)
            index -= 1
        
        # remove dead blocks now
        self.uce()

    def jmp_thread(self) -> None:
        """ Implement jmp threading for uncond jumps """
        
        # we implement some algorithmic idea as in coalescing
        index = self.__num_blocks - 1
        while index > 1:
            block = self.__blocks[index]
            prev_block = self.__blocks[index-1]
            self.__thread(prev_block, block)
        
        self.coalesce()

    def jmp_cond_mod(self) -> None:
        """ Converts cond jmps to uncond jmps """
        for block in self.__blocks:
            self.__check_jcc(block)

        # update succ for each block
        for block in self.__blocks:
            block.update_successors()

        self.jmp_thread()

    def optimization(self) -> None:
        """ Carry out CFG optimizations """
        self.jmp_cond_mod()

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

    # ---------------------------------------------------------------------------#
    # Getter functions for unit tests

    def get_blocks(self) -> List[Block]:
        return self.__blocks

    def get_label_to_blocks(self) -> Dict[str, Block]:
        return self.__labels_to_blocks

    def get_edges(self) -> Dict[str, List[str]]:
        self.__update_edges()
        return self.__successors