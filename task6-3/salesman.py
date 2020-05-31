#!/usr/bin/env python
import sys
import os
import math
from tabulate import tabulate


def repr_mtx(mtx):
    print(tabulate(
        [
            ['M' if c == math.inf or c == 'inf' else c for c in row]
            for row in mtx
        ],
        tablefmt='fancy_grid'
    ))


def get_col(mtx, col):
    return [r[col] for r in mtx]


def transpose(mtx):
    return [
        get_col(mtx, i)
        for i, _ in enumerate(mtx[0])
    ]


def find_most_valuable(mtx):
    _repr = [[str(c) for c in row[:]] for row in mtx[:]]
    res = (0, 0, 0)  # value, row, col
    cols = transpose(mtx)
    for y, row in enumerate(mtx):
        for x, c in enumerate(row):
            if c != 0:
                continue
            minr = min(s for i, s in enumerate(row) if i != x)
            minc = min(s for i, s in enumerate(cols[x]) if i != y)
            value = minr + minc
            _repr[y][x] += f' ({value})'
            if value > res[0]:
                res = (value, y, x)
    print('Values:')
    repr_mtx(_repr)
    print(f'Selected cell: row: {res[1]}; column: {res[2]}.')
    return res


def iter(mtx):
    row_mins = [min(row) for row in mtx]
    row_mins = [0 if it == math.inf else it for it in row_mins]
    print('Row minimums:', row_mins)

    reduced_rows = [
        [c - row_mins[rn] for c in row]
        for rn, row in enumerate(mtx)
    ]
    print('\n\nReduced rows:')
    repr_mtx(reduced_rows)

    col_mins = [min(col) for col in transpose(reduced_rows)]
    col_mins = [0 if it == math.inf else it for it in col_mins]
    print('Col minimums:', col_mins)

    reduced_cols = [
        [c - col_mins[i] for i, c in enumerate(row)]
        for row in reduced_rows
    ]
    print('\n\nReduced cols:')
    repr_mtx(reduced_cols)

    # print(find_most_valuable(reduced_cols))
    value, row, col = find_most_valuable(reduced_cols)
    # reduced_cols[row][col] = reduced_cols[col][row] = math.inf

    return (reduced_cols, row, col)


if __name__ == '__main__':
    args = sys.argv[1:]
    inp_file = args[0]

    with open(inp_file, 'rt') as f:
        lines = [l[:-1] for l in f.readlines()]
        mtx = [
            [math.inf if c == '-' else int(c) for c in line.split()]
            for line in lines
        ]
    print('Input:')
    repr_mtx(mtx)
    city_count = len(mtx)
    cities = list(range(city_count))
    path = []
    orig_mtx = [row[:] for row in mtx[:]]

    while len(path) + 1 < city_count:
        next_mtx, row, col = iter(mtx)
        next_mtx[row][col] = math.inf
        next_mtx[col][row] = math.inf
        path.append(cities[row])
        cities = cities[:row] + cities[row + 1:]
        mtx = [
            row[:col] + row[col + 1:]
            for row in next_mtx[:row] + next_mtx[row + 1:]
        ]
        print('Reduced matrix:')
        repr_mtx(mtx)
        print('\n\n')

    path.append(cities[0])
    path.append(path[0])
    cost = 0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        val = orig_mtx[a][b]
        print(val)
        cost += val
    print('Path:', ' - '.join(str(c + 1) for c in path))
    print('Cost:', cost)
