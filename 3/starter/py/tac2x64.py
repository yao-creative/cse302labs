"""
This is a very simple TAC to x64 assembly pass. It only handles straightline
code and a single main() function.

Usage: python3 tac2asm.py tacfile.json
Produces: tacfile.s (assembly) and tacfile.exe (executable)
Requires: a working gcc
"""

import json, sys, os
from pathlib import Path
from typing import List

"""

Authors: Yi Yao Tan 
         Vrushank Agrawal

"""

class tac2x64:

    def __init__(self, functn: str, tac_instrs: List) -> None:
        self.tac_instr: List = tac_instrs
        self.func_name: str = functn
        self.assembly: List = []
        self.temp_map: dict = {}

    binops = {'add': 'addq',
              'sub': 'subq',
              'mul': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                          f'imulq {rb}',
                                          f'movq %rax, {rd}']),
              'div': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                          f'cqto',
                                          f'idivq {rb}',
                                          f'movq %rax, {rd}']),
              'mod': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                          f'cqto',
                                          f'idivq {rb}',
                                          f'movq %rdx, {rd}']),
              'and': 'andq',
              'or': 'orq',
              'xor': 'xorq',
              'shl': (lambda ra, rb, rd: [f'movq {ra}, %r11',
                                          f'movq {rb}, %rcx',
                                          f'salq %cl, %r11',
                                          f'movq %r11, {rd}']),
              'shr': (lambda ra, rb, rd: [f'movq {ra}, %r11',
                                          f'movq {rb}, %rcx',
                                          f'sarq %cl, %r11',
                                          f'movq %r11, {rd}'])}
    unops = {'neg': 'negq',
            'not': 'notq'}

    jcc = ["je", "jz"     # Src2 == Src1
           "jne", "jnz",  # Src2 != Src1
           "jl", "jnge",  # Src2 < Src1
           "jle", "jng",  # Src2 <= Src1
           "jg", "jnle",  # Src2 > Src1
           "jge", "jnl",  # Src2 >= Src1
           ]

    def lookup_temp(self, temp) -> str:
        """ Returns the value of the temp from the stack 
            while simultaneously creating a hash table """
        assert (isinstance(temp, str) and \
                temp[0] == '%' and \
                temp[1:].isnumeric()), temp
        return self.temp_map.setdefault(temp, f'{-8 * (len(self.temp_map) + 1)}(%rbp)')

    def tac_to_asm(self) -> List:
        """
        Get the x64 instructions correspondign to the TAC instructions
        """

        for instr in self.tac_instrs:
            print(f"instr: {instr}")    # DEBUG
            opcode = instr['opcode']
            args = instr['args']
            result = instr['result']
            if opcode == 'nop':
                pass
            elif opcode == 'Label':
                assert (len(args) == 1), args
                arg = args[0]
                assert (isinstance(arg, str) and \
                        arg.startswith('%.L')), arg
                assert result == None
                self.assembly.append(f'.{self.func_name}{arg[1:]}')    # add label to the assembly
            elif opcode == 'const':
                assert len(args) == 1 and isinstance(args[0], int)
                result = self.lookup_temp(result, self.temp_map)
                self.assembly.append(f'\tmovq ${args[0]}, {result}')
            elif opcode == 'copy':
                assert len(args) == 1
                arg = self.lookup_temp(args[0], self.temp_map)
                result = self.lookup_temp(result, self.temp_map)
                self.assembly.append(f'\tmovq {arg}, %r11')
                self.assembly.append(f'\tmovq %r11, {result}')
            elif opcode in self.binops:
                assert len(args) == 2
                arg1 = self.lookup_temp(args[0], self.temp_map)
                arg2 = self.lookup_temp(args[1], self.temp_map)
                result = self.lookup_temp(result, self.temp_map)
                bin_op = self.binops[opcode]
                if isinstance(bin_op, str):
                    self.assembly.extend([f'\tmovq {arg1}, %r11',
                                          f'\t{bin_op} {arg2}, %r11',
                                          f'\tmovq %r11, {result}'])
                else: 
                    self.assembly.extend(bin_op(arg1, arg2, result))
            elif opcode in self.unops:
                assert len(args) == 1
                arg = self.lookup_temp(args[0], self.temp_map)
                result = self.lookup_temp(result, self.temp_map)
                un_op = self.unops[opcode]
                self.assembly.extend([f'\tmovq {arg}, %r11',
                                      f'\t{un_op} %r11',
                                      f'\tmovq %r11, {result}'])
            elif opcode == 'print':
                assert len(args) == 1
                assert result == None
                arg = self.lookup_temp(args[0], self.temp_map)
                self.assembly.extend([f'\tmovq {arg}, %rdi',
                                      f'\tcallq bx_print_int'])
            elif opcode == 'jmp':
                assert len(args) == 1
                assert result == None
                arg = args[0]
                self.assembly.append(f'\tjmp {args[0]}')

            elif opcode in self.jcc:
                assert len(args) == 1
                assert result == None
                arg = self.lookup_temp(args[0], self.temp_map)
                self.assembly.extend([f'\tjmp {args[0]}'])

            else:       # where did we screw up?
                raise RuntimeError(f'Undefined opcode: {opcode}')
            
        # set the stack size to the number of temporaries we need
        stack_size = len(self.temp_map)
        if stack_size % 2 != 0: 
            stack_size += 1         # 16 byte alignment for x64
        
        # Store the base pointer and initialize the stack pointer 
        self.assembly[:0] = [f'\tpushq %rbp',
                             f'\tmovq %rsp, %rbp',
                             f'\tsubq ${8 * stack_size}, %rsp']

        # Reset the base pointer to the stack pointer
        self.assembly.extend([f'\tmovq %rbp, %rsp',
                              f'\tpopq %rbp',
                              f'\tmovq $0, %rax',     # set return code to 0
                              f'\tretq'])
        return self.assembly

def compile_tac(fname):
    if fname.endswith('.tac.json'):
        rname = fname[:-9]
    elif fname.endswith('.json'):
        rname = fname[:-5]
    else:
        raise ValueError(f'{fname} does not end in .tac.json or .json')
    
    tac_jsn = None
    with open(fname, 'rb') as fp:
        tac_jsn = json.load(fp)
    assert isinstance(tac_jsn, list) and len(tac_jsn) == 1, tac_jsn
    tac_jsn = tac_jsn[0]
    assert 'proc' in tac_jsn and tac_jsn['proc'] == '@main', tac_jsn
    
    x64_asm = tac2x64(tac_jsn['proc'][1:], tac_jsn['body'])     # initialize tac2x64 class here 
    asm = x64_asm.tac_to_asm()
    asm[:0] = [f'\t.text',
               f'\t.globl main',
               f'main:']
    
    xname = rname + '.exe'
    sname = rname + '.s'
    with open(sname, 'w') as afp:
        print(*asm, file=afp, sep='\n')
    os.system(f'gcc -o {xname} {sname} bx_runtime.c')
    print(f'{fname} -> {sname}')
    print(f'{sname} -> {xname}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} tacfile.tac.json')
        sys.exit(1)
    compile_tac(sys.argv[1])
