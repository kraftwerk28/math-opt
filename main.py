#!/usr/bin/env python
#     __              ______                     __  ___   ____ 
#    / /___________ _/ __/ /__      _____  _____/ /_|__ \ ( __ )
#   / //_/ ___/ __ `/ /_/ __/ | /| / / _ \/ ___/ //_/_/ // __  |
#  / ,< / /  / /_/ / __/ /_ | |/ |/ /  __/ /  / ,< / __// /_/ / 
# /_/|_/_/   \__,_/_/  \__/ |__/|__/\___/_/  /_/|_/____/\____/  
#
# Jordan-Gauss resolve method
# Usage: ./main.py input.txt [output_dir]
# Input file format example:
#
# max
# x1   x2   s1   s2   s3  P
# -3   -4   0    0    0   0
# -3   -5   1    0    0   -10
# -5   -3   0    1    0   -10
# 4    7    0    0    1   23
#

import sys
import shutil
from simplex import Simplex


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        sys.exit(1)

    inp = args[0]
    jg = Simplex(inp)
    jg.iterate_full()
    if len(args) > 1:
        shutil.rmtree(args[1])
        jg.dump_matrices(args[1])
