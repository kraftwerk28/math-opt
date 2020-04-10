#!/usr/bin/env python
import re
import sys
from termcolor import colored
from fractions import Fraction as Fr
from tabulate import tabulate

# M = input('Matrix width: ')
# N = input('Matrix height: ')


def step(mtx, pivot):
    N, M = len(mtx), len(mtx[0])
    res = [[None for _ in range(M)] for _ in range(N)]
    px, py = pivot
    pv = mtx[py][px]
    print('pivot (x y):', pv)
    if pv == 0:
        raise Exception('Pivot cannot be zero')
    for i in range(M):
        res[py][i] = Fr(mtx[py][i] / pv).limit_denominator(200)
    for i in range(N):
        res[i][px] = Fr(0)
    res[py][px] = Fr(1)
    for y in range(N):
        if y == py:
            continue
        for x in range(M):
            f1 = Fr()
            res[y][x] = Fr(
                (mtx[y][x] * pv - mtx[py][x] * mtx[y][px]) / pv
            ).limit_denominator(200)
    return res


def read_mtx(string):
    return [
        [Fr(n) for n in s.split()]
        for s in string.split('\n')
        if s
    ]


def print_mtx(mtx, pivot=None):
    print(tabulate(
        [[str(c) for c in row] for row in mtx],
        tablefmt='fancy_grid',
    ))


def write_mtx(fname, mtx):
    open(fname, 'w+').write(
        '\n'.join(' '.join(str(c) for c in row) for row in mtx)
    )


if __name__ == '__main__':
    fname, resname = sys.argv[1:]
    mtx = read_mtx(open(fname, 'r').read())
    pivot = [int(s) for s in re.split(r'[, ]+', input('pivot: '))]
    print_mtx(mtx)
    res = step(mtx, pivot)
    print_mtx(res)
    write_mtx(resname, res)
