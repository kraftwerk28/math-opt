#!/usr/bin/env python
# Jordan-Gauss resolve method
# Usage: ./main.py input.txt output.txt
# Input file must contain matrix w/ whitespace-separated numbers
# and line-break separated rows
import sys
from JG import JG

if __name__ == '__main__':
    if len(sys.argv[1:]) < 2:
        sys.exit(1)
    inp, outdir = sys.argv[1:]

    jg = JG(inp, is_maximizing=True)
    jg.iterate_full()
    jg.dump_matrices(outdir)
