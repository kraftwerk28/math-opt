import os
import sys
from fractions import Fraction
from tabulate import tabulate
import math
from utils import *


class JG:
    def __init__(self, input_file: str = None, is_maximizing=True):
        self.iters = []
        self.headers = []
        self.free_variables = []  # s1, s2, s3 etc
        self.target_row_idx = 0
        self.pivots = []
        self.is_maximizing = is_maximizing  # False -> min; True -> max

        if input_file is None:
            return

        with open(input_file, 'rt') as f:
            max_min, *mtx = [
                s[:-1].split()
                for s in f.readlines()
                if s.strip()
            ]
            self.is_maximizing = max_min[0] == 'max'
            has_header = mtx[0][0][0].isalpha()
            if has_header:
                self.headers = mtx[0]
                self.free_variables = [
                    h for h in mtx[0]
                    if not h.startswith('x') and h != 'P'
                ]
                tdata = mtx[1:]
            else:
                tdata = mtx
            parsed = [[fr(c) for c in row] for row in tdata]
            self.iters.append(parsed)

    def iterate(self):
        lastiter = self.iters[-1]
        piv = self._choose_pivot()
        self.pivots.append(
            f'pivot: {str(lastiter[piv[0]][piv[1]])} ({piv[0]}; {piv[1]})'
        )
        next_iter = iter_mtx(lastiter, piv)
        self.iters.append(next_iter)
        if self.free_variables and self.headers:  # Swap variables label
            row, col = piv
            t = self.free_variables[row - 1]
            self.free_variables[row - 1] = self.headers[col]
            self.headers[col] = t

    def iterate_full(self):
        self.print_iter(-1)
        piv = self._choose_pivot()
        iter_mtx(self.iters[-1], piv)

        def check_iter_end():
            return any(
                c < 0 if self.is_maximizing else c > 0
                for c in self.iters[-1][self.target_row_idx][:-1]
            )
        while check_iter_end():
            self.iterate()
            self.print_iter(-1)
            input()

    def add_mtx(self, mtx):
        self.iters.append(mtx)

    def print_iter(self, i=0):
        num = i + 1 if i > -1 else len(self.iters) + i
        print(f'Iter #{num}:')
        if self.pivots:
            print(self.pivots[i])

        headers = [''] + self.headers
        sider = ['Z', *self.free_variables]

        if self.free_variables:
            tdata = [
                [var] + [str(c) for c in rest]
                for var, rest in zip(sider, self.iters[i])
            ]
        else:
            tdata = [
                [str(c) for c in row]
                for row in self.iters[i]
            ]
        print(tabulate(tdata, headers=headers, tablefmt='grid'))

    def _choose_pivot(self) -> (int, int):
        lastiter = self.iters[-1]

        top_row = lastiter[self.target_row_idx][:-1]
        col_idx = top_row.index(
            min(top_row) if self.is_maximizing else max(top_row)
        )

        col = [row[col_idx] for row in lastiter]
        rates = [
            (row[-1] / col[i])
            if (col[i] > 0 and i != self.target_row_idx)
            else math.inf
            for i, row in enumerate(lastiter)
        ]
        row_idx = rates.index(min(rates))
        return (row_idx, col_idx)

    def dump_matrices(self, dirpath):
        os.makedirs(dirpath, exist_ok=True)
        for i, it in enumerate(self.iters):
            path = os.path.join(dirpath, f'iter{i}.txt')
            with open(path, 'w+') as f:
                data = '\n'.join(
                    ''.join(str(it).rjust(6)
                            for it in row) for row in it
                )
                f.write(data + '\n')


if __name__ == '__main__':
    if len(sys.argv[1:]) < 2:
        sys.exit(1)
    inp, outdir = sys.argv[1:]

    jg = JG(inp, is_maximizing=True)
    jg.iterate_full()
    jg.dump_matrices(outdir)
