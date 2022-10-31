import unittest
import os
from tac_cfopt import *

dirname, filename = os.path.split(os.path.abspath(__file__))

class testUce(unittest.TestCase):

    def setUp(self):
        fname = "../tac_examples/dead_code.tac.json"

        # we only check one function in the example
        with open(fname, 'r') as f:
            tac_instr = json.load(f)[0]
        label = "0"
        basic_blocks = CFG_creator(tac_instr["proc"][1:], tac_instr["body"], label).return_blocks()
        self.cfg = CFG(basic_blocks, tac_instr["proc"][1:])

    def test_edges_init(self):
        expected_edges = {'%.L1': ['%.L4'],
                         '%.L2': ['%.L3'],
                         '%.L3': ['%.L4'],
                         '%.L4': ['%.L5'],
                         '%.L5': []}
        self.assertEqual(self.cfg.get_edges(), expected_edges)

    def test_uce_skip_two(self):
        expected_edges = {'%.L1': ['%.L4'],
                          '%.L4': ['%.L5'],
                          '%.L5': []}
        self.cfg.uce()
        self.assertEqual(self.cfg.get_edges(), expected_edges)
        self.assertEqual(len(self.cfg.get_blocks()), 3)

    def tearDown(self):
        del self.cfg


class testJmpCond(unittest.TestCase):

    def prepfile(self, fname):
        with open(fname, 'r') as f:
            tac_instr = json.load(f)[0]
        label = "0"
        basic_blocks = CFG_creator(tac_instr["proc"][1:], tac_instr["body"], label).return_blocks()
        return CFG(basic_blocks, tac_instr["proc"][1:])

    def setUp(self):
        fname1 = "../tac_examples/cond_jmps.tac.json"
        self.cfg1 = self.prepfile(fname1)

        fname2 = "../tac_examples/cond_jmps2.tac.json"
        self.cfg2 = self.prepfile(fname2)

        fname3 = "../tac_examples/cond_update_temp.tac.json"
        self.cfg3 = self.prepfile(fname3)

    def test_cond_jmp_implication(self):
        self.cfg1.jmp_cond_mod()
        self.assertEqual(len(self.cfg1.get_blocks()), 5)

        node2 = self.cfg1.get_label_to_blocks()["%.L2"]
        expected_jmp = {"opcode":"jmp", "args":["%.L3"], "result":None}

        self.assertEqual(node2.instructions()[1], expected_jmp)
        self.assertEqual(len(node2.instructions()), 2)

    def test_cond_jmp_negation(self):
        self.cfg2.jmp_cond_mod()
        self.assertEqual(len(self.cfg2.get_blocks()), 4)

        node2 = self.cfg2.get_label_to_blocks()["%.L2"]
        expected_jmp = {"opcode":"jmp", "args":["%.L30"], "result":None}

        self.assertEqual(node2.instructions()[1], expected_jmp)
        self.assertEqual(len(node2.instructions()), 2)

    def test_updating_temporary(self):
        self.cfg3.jmp_cond_mod()
        self.assertEqual(len(self.cfg2.get_blocks()), 5)

        node2 = self.cfg3.get_label_to_blocks()["%.L2"]
        expected_jmp = {"opcode":"jz", "args":["%1", "%.L3"], "result":None}
        self.assertEqual(node2.instructions()[2], expected_jmp)
        self.assertEqual(len(node2.instructions()), 4)

    def tearDown(self):
        del self.cfg1
        del self.cfg2
        del self.cfg3


class testCoalescing(unittest.TestCase):
    
    def prepfile(self, fname):
        with open(fname, 'r') as f:
            tac_instr = json.load(f)[0]
        label = "0"
        basic_blocks = CFG_creator(tac_instr["proc"][1:], tac_instr["body"], label).return_blocks()
        return CFG(basic_blocks, tac_instr["proc"][1:])

    def setUp(self):
            fname1 = "../tac_examples/coalescing.tac.json"
            self.cfg1 = self.prepfile(fname1)

    def test_coalesce_blocks(self):
        self.assertEqual(len(self.cfg1.get_blocks()), 7)
        self.cfg1.coalesce()
        self.assertEqual(len(self.cfg1.get_blocks()), 3)
    
    def tearDown(self):
        del self.cfg1


class testSerialization(unittest.TestCase):
    
    def prepfile(self, fname):
        with open(fname, 'r') as f:
            tac_instr = json.load(f)[0]
        label = "0"
        basic_blocks = CFG_creator(tac_instr["proc"][1:], tac_instr["body"], label).return_blocks()
        return CFG(basic_blocks, tac_instr["proc"][1:])

    def setUp(self):
            fname1 = "../tac_examples/fib20.tac.json"
            self.cfg1 = self.prepfile(fname1)

            fname2 = "../tac_examples/cond_jmps2.tac.json"
            self.cfg2 = self.prepfile(fname2)

            fname3 = "../tac_examples/cond_update_temp.tac.json"
            self.cfg3 = self.prepfile(fname3)

    def test_remove_jmp(self):
        self.cfg1.uce()
        self.cfg1.jmp_cond_mod()
        self.cfg1.coalesce()
        res = self.cfg1.serialized_tac()

        jmp_count_init = 0
        for node in self.cfg1.get_blocks():
            for instr in node.instructions():
                if instr["opcode"] == "jmp":
                    jmp_count_init += 1
        self.assertEqual(jmp_count_init, 3)

        jmp_count = 0
        for line in res:
            if line["opcode"] == "jmp":
                jmp_count += 1
        
        self.assertEqual(jmp_count, 2)
    
    def tearDown(self):
        del self.cfg1
        del self.cfg2
        del self.cfg3


if __name__ == "__main__":
    unittest.main()
