from fractions import Fraction


def fr(value): return Fraction(value).limit_denominator(200)


def iter_mtx(mtx, pivot):  # Does one iteration on matrix
    rows, cols = len(mtx), len(mtx[0])
    res = [[None for _ in range(cols)] for _ in range(rows)]
    py, px = pivot  # Pivot location
    pv = mtx[py][px]  # Pivot value

    if pv == 0:
        raise Exception('Pivot cannot be zero')
    for i in range(cols):  # Divide whole row by pivot value
        res[py][i] = fr(mtx[py][i] / pv)
    for i in range(rows):  # Zero-ify whole column on pivot value
        res[i][px] = fr(0)
    res[py][px] = fr(1)  # Self-divide to pivot point
    for y in range(rows):
        if y == py:
            continue
        for x in range(cols):
            a, b, c, d = mtx[y][x], mtx[y][px], mtx[py][x], pv
            res[y][x] = fr((a * d - b * c) / pv)
    return res
