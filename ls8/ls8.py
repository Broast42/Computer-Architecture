#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("Usage: example.py filename")
    sys.exit(3)
cpu.load(sys.argv[1])
cpu.run()