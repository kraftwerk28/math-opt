#!/usr/bin/env python
import os
import sys
from fractions import Fraction
from tabulate import tabulate
import math
from utils import *


class Simplex:
    def __init__(self, input_file: str = None):
        self.iters = []
        self.headers = []
        self.orig_headers = []  # Starting headers from input file, immutable
        self.free_variables = []  # s1, s2, s3 etc
        self.target_row_idx = 0  # Z-equation row index (usually first row)
        self.pivots = []  # Dumped pivot points just for logging
        self.doubling = False

        if input_file is None:
            return

        with open(input_file, 'rt') as f:
            max_min, *mtx = [
                s[:-1].split()
                for s in f.readlines()
                if s.strip()
            ]
            if max_min[0] not in ('max', 'min'):
                print('Missing min/max specifier.')
                sys.exit(1)
            self.is_maximizing = max_min[0] == 'max'
            has_header = mtx[0][0][0].isalpha()
            if has_header:
                self.headers = mtx[0]
                self.orig_headers = self.headers[:]
                if any(s[0] == 'r' for s in self.headers):
                    self.doubling = True
                    self.is_maximizing = False
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
        if self.free_variables and self.headers:  # Swap variable labels
            row, col = piv
            t = self.free_variables[row - 1]
            self.free_variables[row - 1] = self.headers[col]
            self.headers[col] = t

    def iterate_full(self):
        self.print_iter(-1)
        piv = self._choose_pivot()
        iter_mtx(self.iters[-1], piv)

        while self._check_iter_ended():
            self.iterate()
            self.print_iter(-1)
            if len(self.iters) > 40:  # Probably infinite loop
                break
        if self.doubling:
            print('\nPerforming second stage of doubling simplex method...')
            lastiter = self.iters[-1]
            r_indices = [
                i for i, it in enumerate(self.orig_headers)
                if it.startswith('r')
            ]
            self.headers = [
                c for i, c in enumerate(self.orig_headers)
                if i not in r_indices
            ]
            next_iter = [
                [c for i, c in enumerate(row) if i not in r_indices]
                for row in lastiter[1:]
            ]
            self.free_variables = self.free_variables[1:]
            self.iters.append(next_iter)
            self.is_maximizing = True
            self.doubling = False
            self.iterate_full()

    def add_mtx(self, mtx):
        self.iters.append(mtx)

    def _check_iter_ended(self):
        return any(
            c < 0 if self.is_maximizing else c > 0
            for c in self.iters[-1][self.target_row_idx][:-1]
        )

    def print_iter(self, i=0):
        num = i + 1 if i > -1 else len(self.iters) + i
        print(f'\nIteration #{num}:')
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
        print(tabulate(tdata, headers=headers, tablefmt='psql'))

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
        print('Dumping data to files...')
        os.makedirs(dirpath, exist_ok=True)
        for i, it in enumerate(self.iters):
            path = os.path.join(dirpath, f'iter{i}.txt')
            with open(path, 'w+') as f:
                data = '\n'.join(
                    ''.join(
                        str(it).ljust(6)
                        for it in row
                    ).strip() for row in [self.headers] + it
                )
                f.write(data + '\n')
