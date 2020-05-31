import math
from tabulate import tabulate

with open('comiviy.txt', 'r') as f:
    lines = [l[:-1] for l in f.readlines() if l.strip()]
tdata = []
citieset = set()
for l in lines:
    fr, to, v = l.split()
    citieset.add(fr)
    citieset.add(to)
    tdata.append((fr, to, int(v)))
cities = list(citieset)
cities.sort()
mtx = [[0 for _ in cities] for _ in cities]
for fr, to, v in tdata:
    mtx[cities.index(fr)][cities.index(to)] = v

print(tabulate(
    ([cities[rn]] + [c if c != 0 else ' ' for c in row] for rn, row in enumerate(mtx)),
    tablefmt='fancy_grid',
    headers=cities
))

with open('converted.txt', 'w+') as f:
    rep = '\n'.join(
        ''.join(('-' if c == 0 else str(c)).ljust(3) for c in row) for row in mtx
    )
    f.write(rep + '\n')
