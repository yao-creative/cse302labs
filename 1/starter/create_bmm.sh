#!/bin/sh
python3 ast2tac.py arithops.bx.json --bmm arithopsbmm.tac.json
python3 ast2tac.py bitops.bx.json --bmm bitopsbmm.tac.json
python3 ast2tac.py empty.bx.json --bmm emptybmm.tac.json
python3 ast2tac.py example.bx.json --bmm examplebmm.tac.json
python3 ast2tac.py fib10.bx.json --bmm fib10bmm.tac.json
python3 ast2tac.py print42.bx.json --bmm print42bmm.tac.json

python3 tac2asm.py arithopsbmm.tac.json 
python3 tac2asm.py bitopsbmm.tac.json
python3 tac2asm.py emptybmm.tac.json
python3 tac2asm.py examplebmm.tac.json
python3 tac2asm.py fib10bmm.tac.json
python3 tac2asm.py print42bmm.tac.json

chmod ugo+rwx arithopsbmm.exe 
chmod ugo+rwx bitopsbmm.exe
chmod ugo+rwx emptybmm.exe
chmod ugo+rwx examplebmm.exe
chmod ugo+rwx fib10bmm.exe
chmod ugo+rwx print42bmm.exe

echo "bmm created"