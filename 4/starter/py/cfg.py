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
        self.__label: str = self.__instrs[0]["args"][0]
        self.__successors: List[str] = list()
        self.__pred: List[str] = list()
        self.__cond_jmps: List[Tuple[int, dict]] = list()
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

    def update_cond_jmps(self) -> None:
        """ Updates list of all cond jumps """
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
                jccs_with_temp.append((index, instr))
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

    def get_block_label(self) -> str:
        """ Returns the name of the block's label """
        return self.__label

    def set_succ(self, succ: List[str]) -> None:
        """ Sets the successor for the curr block """
        self.__successors = succ

    def set_pred(self, preds: List[str]) -> None:
        """ Sets the predecessor for the curr block """
        self.__pred = preds

    def successors(self) -> List[str]:
        """ Returns all successors for current block """
        return self.__successors

    def predecessors(self) -> list:
        """ Returns all predecessors for current block """
        return self.__pred

    def has_one_succ(self) -> bool:
        """ If block has one succ return True """
        # print("succ", self.__successors)
        return len(self.__successors) == 1

    def has_one_pred(self) -> bool:
        """ If blokc has one pred return True """
        # print("pred", self.__pred)
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
        self.__labels_to_blocks: Dict[str, Block] = {block.get_block_label(): block for block in self.__blocks}
        self.__predecessors: Dict[str, List[str]] = dict()
        self.__deleted_labels: Set[str] = set()
        self.__ret_blocks: List[Block] = list()
        self.__update_graph()

    # ---------------------------------------------------------------------------#
    # Helper functions

    def __update_edges(self) -> None:
        """ Updates all edges in cfg blocks """
        edges = {}
        for block in self.__blocks:
            # block_lab = block.get_block_label()
            # print(block_lab)
            dest = []
            # if block_lab == "%.L10":
            #     print(block.instructions())
            for instr in block.instructions():
                if instr["opcode"] in Block.jccs:
                    if instr["args"][-1] not in dest:
                        dest.append(instr["args"][-1])
            edges[block.get_block_label()] = dest
            # if block_lab == "%.L10":
            #     print(dest)
            block.set_succ(dest)
        self.__successors = edges

    def __update_pred_edges(self) -> None:
        """ Updates the pred graph in the blocks """
        pred_graph = {block.get_block_label(): [] for block in self.__blocks}
        for block in self.__blocks:
            # print(pred_graph)
            # print(block.successors())
            for label in block.successors():
                assert(label in pred_graph), f"unidentified block label {label}"
                pred_graph[label].append(block.get_block_label())
        self.__predecessors = pred_graph
        # update pred list in every block
        for lab, preds in pred_graph.items():
            self.__labels_to_blocks[lab].set_pred(preds)

    def __next(self, label: str) -> List[str]:
        """ Returns the succ labels of the curr label """
        return self.__successors[label]

    def __prev(self, block_lab: str) -> List[str]:
        """ Returns the predecessor blocks for the current block """
        pred_labels = self.__predecessors[block_lab]
        return pred_labels

    def __update_graph(self) -> None:
        """ updates edges in the CFG graph """
        # update edges
        self.__update_edges()
        # print("successors: ", self.__successors)
        # print("predecessors: ", self.__predecessors)
        # print("blocks remaining: ", [block.get_block_label() for block in self.__blocks])
        # update pred graph
        self.__update_pred_edges()
        # print("successors: ", self.__successors)
        # print("predecessors: ", self.__predecessors)

    def __del_block(self, block: Block) -> None:
        """ Delete the given block because it has no pred """
        self.__blocks.remove(block)
        self.__num_blocks = len(self.__blocks)
        del self.__labels_to_blocks[block.get_block_label()]
        self.__entry_block = self.__blocks[0]

    def __coalesce_blocks(self, block1: Block, block2: Block) -> Block:
        """ Coalesce and return the first block """
        block1.remove_last_jmp()
        block1.add_instrs(block2.instructions()[1:])
        return block1

    def __coalescable(self, block1: Block, block2: Block) -> bool:
        """ Checks if given blocks are coalescable """
        if block1.has_one_succ() and block2.has_one_pred():
            assert(block1.last_instr_opcode() == "jmp"), f"Last instr in block is not jmp: {block2.instructions()}"
            assert(block2.last_instr_opcode() in ["jmp", "ret"]), f"Last instr in block is not jmp: {block2.instructions()}"
            if block1.successors()[0] == block2.get_block_label():
                if block2.predecessors()[0] == block1.get_block_label():
                    return True
        return False

    def __thread(self, block1: Block, block2: Block) -> None:
        """ Threads two blocks """
        # block2 can only have 2 instr including label and jmp
        if len(block2.instructions()) == 2 and block2.last_instr_opcode() == "jmp":
            # block2 can only have one pred
            if len(self.__prev(block2.get_block_label())) == 1:
                assert(block1.last_instr_opcode() == "jmp"), f"Last instr in block is not jmp: {block2.instructions()}"
                # the two blocks should be connected to each other
                if block1.last_instr_label() == block2.get_block_label():
                    # print(block1.get_block_label(), block2.get_block_label())
                    block1.remove_last_jmp()
                    block1.add_jmp(block2.last_instr_label())

    __jcc_direct_implication = {"jz":["jz"], "jnz":["jnz"],
                    "jl":["jl", "jle", "jnz"], "jle":["jle"],
                    "jnl":["jnl"], "jnle":["jnle", "jnl", "jnz"],}

    __jcc_neg_implications = {"jz":["jl", "jnle", "jnz"], "jnz":["jz"],
                 "jl":["jnl", "jnle", "jz"], "jle":["jnle"],
                 "jnl":["jl"], "jnle":["jz", "jl", "jle"],}

    def __check_jcc(self, block: Block) -> None:
        """ Checks and updates block if it has removable cond jmp """
        jcc_instrs = block.get_cond_jmps()
        # print(jcc_instrs)
        for index, instr in jcc_instrs:
            dest_block_lab = instr["args"][-1]
            dest_block = self.__labels_to_blocks[dest_block_lab]
            temp = instr["args"][0]         # temporary compared in the jcc instr
            jcc = instr["opcode"]           # jcc command
            
            # print(self.__prev(dest_block_lab))
            # print(block.get_block_label())

            # if dest block has > one pred we can't modify the instr
            if self.__prev(dest_block_lab) != [block.get_block_label()]:
                break
            
            # if no jcc in the dest block uses the temp for comparison, we can skip
            # print(dest_block)
            jccs_with_temp = dest_block.jcc_with_temp(temp)
            # print(jccs_with_temp)
            if jccs_with_temp == []:
                break
            
            # need to check if temp is modified in any dest instr before jcc
            prev_index = 0
            # need to delete all negations of curr jcc instr -> always False
            instr_index_to_delete = []
            
            for dest_index, dest_instr in jccs_with_temp:
                # if the temp has been modified befor jcc instr then break
                if dest_block.is_temp_modified(prev_index, dest_index, temp):
                    break

                # if jcc instr is a direct implication then it will be True
                if dest_instr["opcode"] in self.__jcc_direct_implication[jcc]:
                    dest_lab = dest_instr["args"][-1]
                    # delete all instr after curr jcc
                    dest_block.del_after_cond_jmp(dest_index)
                    # add uncond jmp instr to label of deleted jcc instr
                    dest_block.add_jmp(dest_lab)
                    break
                
                # if jcc instr is a direct neg implication then it will be False
                if dest_instr["opcode"] in self.__jcc_neg_implications[jcc]:
                    # add the instr to be deleted later
                    # print(dest_index, dest_instr)
                    instr_index_to_delete.append(dest_index)
                
                prev_index = dest_index+1

            # delete False cond jmps in reverse
            for index in instr_index_to_delete[::-1]:
                dest_block.del_cond_jmp(index)

            # update cond jmps list in the block
            dest_block.update_cond_jmps()

    # ---------------------------------------------------------------------------#
    # CFG Operations

    def __uce(self) -> None:
        """ Unreachable Code Elimination """
        visited_blocks = {self.__entry_block.get_block_label()}
        to_visit = self.__entry_block.successors()
        # print("successors: ", self.__successors)
        # print("predecessors: ", self.__predecessors)
        # print("blocks remaining: ", [block.instructions() for block in self.__blocks if block.get_block_label() == "%.L10"])
        # mark UC
        while len(to_visit) > 0:
            label = to_visit.pop()
            if label not in visited_blocks:
                visited_blocks.add(label)
                for lab in self.__next(label):
                    if lab != label and lab not in to_visit: 
                        to_visit.append(lab)
        # now delete UC
        to_delete = []
        for block in self.__blocks:
            if block.get_block_label() not in visited_blocks:
                to_delete.append(block)
        for block in to_delete:
            self.__deleted_labels.add(block.get_block_label())
            self.__del_block(block)

        # print("successors: ", self.__successors)
        # print("predecessors: ", self.__predecessors)
        # print("blocks remaining: ", [block.instructions() for block in self.__blocks if block.get_block_label() == "%.L10"])
        # for block in self.__blocks:
        #     print(block.instructions())
        print("UCE done")

        self.__update_graph()

    def __coalesce(self) -> None:
        """ Coalesce two blocks if one succ and one pred """
        # we go bottom-up because if two blocks can be coalesced then 
        # the bottom block is shifted to the one above. This is faster to
        # implement than top-bottom where we'll need to run nested for loop 
        index = self.__num_blocks-1
        while index > 0:
            block = self.__blocks[index]
            prev_block = self.__blocks[index-1]
            if self.__coalescable(prev_block, block):
                self.__blocks[index-1] = self.__coalesce_blocks(prev_block, block)
            index -= 1
        self.__update_graph()

        # for block in self.__blocks:
        #     print(block.instructions())
        print("Coalesce done")

        self.__uce()

    def __jmp_thread(self) -> None:
        """ Implement jmp threading for uncond jumps """       
        # we implement same idea described in coalescing
        index = self.__num_blocks - 1
        while index > 0:
            block = self.__blocks[index]
            prev_block = self.__blocks[index-1]
            self.__thread(prev_block, block)
            index -= 1
        self.__update_graph()

        # for block in self.__blocks:
        #     print(block.instructions())
        print("jmp thread done")
        
        self.__uce()
        self.__coalesce()

    def __jmp_cond_mod(self) -> None:
        """ Jump threading to convert cond jmps to uncond jmps """     
        for block in self.__blocks:
            self.__check_jcc(block)
            if block not in self.__ret_blocks:
                self.__ret_blocks.append(block)
        self.__update_graph()

        # for block in self.__blocks:
        #     print(block.instructions())
        print("jmp cond done")

        self.__uce()
        self.__jmp_thread()

    def optimization(self) -> None:
        """ Carry out CFG optimizations """
        self.__jmp_cond_mod()
        # exit(0)

    # ---------------------------------------------------------------------------#
    # Serialization

    def __serialize(self) -> List[Block]:
        """ Serialisation from CFG to TAC """
        curr_block: Block = self.__entry_block
        scheduled: List[Block] = list()
        remaining_blocks: List[Block] = self.__blocks.copy()
        # print(self.__labels_to_blocks)
        
        # All blocks end with jmp or ret so we string jmp blocks together
        while len(scheduled) < self.__num_blocks:
            scheduled.append(curr_block)
            remaining_blocks.remove(curr_block)
            last_instr_code = curr_block.last_instr_opcode()
            # once we hit a ret block we must add first unscheduled block
            if last_instr_code == "ret":
                if len(remaining_blocks) > 0:
                    curr_block = remaining_blocks[0]
                continue
            assert(last_instr_code == "jmp"), f"Last instr should be jmp: {curr_block.instructions()[-1]}"
            next_lab = curr_block.last_instr_label()
            curr_block = self.__labels_to_blocks[next_lab]
            # if curr block is a loop then we get out of it if blocks remain
            if curr_block in scheduled:
                if len(remaining_blocks) > 0:
                    curr_block = remaining_blocks[0]
        
        return scheduled

    def serialized_tac(self) -> List[dict]:
        """ Returns serialized Blocks converted to TAC form """
        blocks = self.__serialize()
        tac_instrs = []
        for block in blocks:
            tac_instrs += block.instructions()
        return tac_instrs
