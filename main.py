#!/usr/bin/env python
# Jordan-Gauss resolve method
# Usage: ./main.py input.txt output.txt
# Input file must contain matrix w/ whitespace-separated numbers
# and line-break separated rows

import re
import os
import sys
try:
    from fractions import Fraction as Fr
    from tabulate import tabulate
except ImportError as e:
    print('Required dependencies: `fractions`, `tabulate`.')
    sys.exit(1)



def read_mtx(fname):
    ls = open(fname, 'r').readlines()
    # with open(fname, 'r').readlines() as f:
    return [[Fr(n) for n in s.split()] for s in ls if s]


def print_mtx(mtx, pivot=None):
    print(tabulate(
        [[str(c) for c in row] for row in mtx],
        tablefmt='grid',
    ))


def write_mtx(fname, mtx):
    open(fname, 'w+').write(
        '\n'.join('\t'.join(str(c) for c in row) for row in mtx)
    )


if __name__ == '__main__':
    infile, outdir = sys.argv[1:]
    mtx = read_mtx(infile)
    pivot = (
        int(s)
        for s in re.split(r'[, ]+', input('pivot postition (x y): '))
    )
    print_mtx(mtx)
    res = step(mtx, pivot)
    print_mtx(res)
    write_mtx(outfile, res)
