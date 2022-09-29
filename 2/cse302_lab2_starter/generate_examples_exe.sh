#!/bin/bash
#bx2asm.py <input-.bx-file> <--tmm||--bmm> <output-.tac.json-file>

for file in $(find regression -name "*.bx"); do
    echo $file
    python3 py/bx2asm.py $file --tmm $file.tmm.tac.json
    python3 py/bx2asm.py $file --bmm $file.bmm.tac.json
done
