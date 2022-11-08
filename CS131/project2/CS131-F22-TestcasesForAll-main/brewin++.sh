#!/bin/bash

PYCMD=$(cat <<EOF
from interpreterv2 import Interpreter
import sys
program = []
f = open(sys.argv[1])
for line in f:
    program.append(line.rstrip())
f.close()
interpreter = Interpreter()
interpreter.run(program)
EOF
)

python3 -c "$PYCMD" $1