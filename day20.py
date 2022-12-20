import copy
import sys

from itertools import cycle

import utils

test_mode = len(sys.argv) > 1
input_file = f'day20_{sys.argv[1]}_input.txt' if test_mode else f'day20_input.txt'
data = utils.input_as_ints(input_file)

orig = list(enumerate(data))
mixed = copy.deepcopy(orig)

s = len(data) - 1

for j, n in orig:
    i = mixed.index((j, n))
    new_i = (i + n) % s
    
    mixed.pop(i)
    mixed.insert(new_i, (j, n))

    # print([m[1] for m in mixed])
   
i0 = mixed.index((data.index(0), 0))
_, n1000 = mixed[(i0+1000)%(s+1)]
_, n2000 = mixed[(i0+2000)%(s+1)]
_, n3000 = mixed[(i0+3000)%(s+1)]
print("Coordinates:", n1000, n2000, n3000)
print("Part1: ", n1000 + n2000 + n3000)

# Part 2
decryption_key = 811589153
new_data = [(i, n*decryption_key) for i, n in orig]
mixed = copy.deepcopy(new_data)

# s = s-1

# print([m[1] for m in mixed])

for _ in range(10):
    for j, n in new_data:
        i = mixed.index((j, n))
        new_i = (i + n) % s
        
        mixed.pop(i)
        mixed.insert(new_i, (j, n))

    # print([m[1] for m in mixed])
   
i0 = mixed.index((data.index(0), 0))
_, n1000 = mixed[(i0+1000)%(s+1)]
_, n2000 = mixed[(i0+2000)%(s+1)]
_, n3000 = mixed[(i0+3000)%(s+1)]
print("Coordinates:", n1000, n2000, n3000)
print("Part2: ", n1000 + n2000 + n3000)
