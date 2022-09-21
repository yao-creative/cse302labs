#!/bin/sh
python3 ast2tac.py arithops.bx.json --tmm arithopstmm.tac.json
python3 ast2tac.py bitops.bx.json --tmm bitopstmm.tac.json
python3 ast2tac.py empty.bx.json --tmm emptytmm.tac.json
python3 ast2tac.py example.bx.json --tmm exampletmm.tac.json
python3 ast2tac.py fib10.bx.json --tmm fib10tmm.tac.json
python3 ast2tac.py print42.bx.json --tmm print42tmm.tac.json

python3 tac2asm.py arithopstmm.tac.json 
python3 tac2asm.py bitopstmm.tac.json
python3 tac2asm.py emptytmm.tac.json
python3 tac2asm.py exampletmm.tac.json
python3 tac2asm.py fib10tmm.tac.json
python3 tac2asm.py print42tmm.tac.json

chmod ugo+rwx arithopstmm.exe 
chmod ugo+rwx bitopstmm.exe
chmod ugo+rwx emptytmm.exe
chmod ugo+rwx exampletmm.exe
chmod ugo+rwx fib10tmm.exe
chmod ugo+rwx print42tmm.exe

echo "tmm created"
