import copy
import sys

from itertools import cycle

import utils

test_mode = len(sys.argv) > 1
input_file = f'day20_{sys.argv[1]}_input.txt' if test_mode else f'day20_input.txt'
data = utils.input_as_ints(input_file)

orig = list(enumerate(data))
mixed = copy.deepcopy(orig)

s = len(data)

for j, n in orig:
    i = mixed.index((j, n))
    new_i = (i + n)
    
    # correct for wrapping - add or subtract 1 every time we go circle round
    if n != 0 and new_i <= 0:
        if new_i // s < 0:
            new_i += new_i // s
        else:
            new_i -= 1
        new_i = new_i % s
    elif n != 0 and new_i >= s:
        if new_i // s > 0:
            new_i += (new_i // s)
        else:
            new_i += 1
        new_i = new_i % s

    mixed.pop(i)
    mixed.insert(new_i, (j, n))

    # print([m[1] for m in mixed])
   
i0 = mixed.index((data.index(0), 0))
_, n1000 = mixed[(i0+1000)%s]
_, n2000 = mixed[(i0+2000)%s]
_, n3000 = mixed[(i0+3000)%s]
print("Coordinates:", n1000, n2000, n3000)
print("Part1: ", n1000 + n2000 + n3000)
