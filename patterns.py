from __future__ import annotations
import numpy as np

__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

## Paterns for game of life

# First we generate the still lifes

block = np.array([[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]])
beehive = np.array([[0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0, 0],
                    [0, 1, 0, 0, 1, 0],
                    [0, 0, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0]])
loaf = np.array([[0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 1, 0, 0],
                 [0, 1, 0, 0, 1, 0],
                 [0, 0, 1, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0]])
boat = np.array([[0, 0, 0, 0, 0],
                 [0, 1, 1, 0, 0],
                 [0, 1, 0, 1, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0]])
tub = np.array([[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]])


# Now we generate the oscillators

blinker = np.array([[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0]])
toad = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

beacon = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
])

glider = {
    'NE': np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]),
    'NW': np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0]
]),
    'SW': np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]),
    'SE': np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
}

lwws = {
    'NE': np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]),
    'NW': np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])
}

import numpy as np
import re

def rle_to_numpy(rle_string):
    lines = rle_string.split('\n')
    grid = []
    row = []
    for line in lines:
        if line.startswith('#') or line == '':
            continue
        elif line.startswith('x'):
            dimensions = re.findall(r'\d+', line)
            x, y = int(dimensions[0]), int(dimensions[1])
        else:
            repeat = 1
            for char in line:
                if char.isdigit():
                    repeat = int(char)
                elif char == 'b':
                    row.extend([0]*repeat)
                    repeat = 1
                elif char == 'o':
                    row.extend([1]*repeat)
                    repeat = 1
                elif char == '$':
                    row.extend([0]*(x - len(row)))
                    grid.append(row)
                    row = []
    grid.extend([[0]*x]*(y - len(grid)))
    return np.array(grid)

rle_string = """
#N 20cellquadraticgrowth.rle
#O dani, 2022
#C https://conwaylife.com/wiki/20-cell_quadratic_growth
#C https://www.conwaylife.com/patterns/20cellquadraticgrowth.rle
x = 97, y = 33, rule = B3/S23
94bo$92bobo$94b2o6$88b3o11$96bo$95b2o8$3bob2o$2bo3bo$bo$bo$obo!
"""

quad = rle_to_numpy(rle_string)


gun = np.zeros((3, 49))
gun[1, :] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

replicator = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
])


p2 = rle_to_numpy(
"""
#N Puffer 2
#O Bill Gosper
#C An orthogonal period 140 c/2 puffer. The second puffer to be found. It uses two lightweight spaceships to escort a B-heptomino.
#C www.conwaylife.com/wiki/index.php?title=Puffer_2
x = 18, y = 5, rule = b3/s23
b3o11b3o$o2bo10bo2bo$3bo4b3o6bo$3bo4bo2bo5bo$2bo4bo8bo!
"""
)