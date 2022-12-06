import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day06_test_input.txt" if test_mode else f"day06_input.txt"
data = utils.input_as_string(input_file)

# Part 1
i = 0
while i < len(data):
    if len(set(data[i : i + 4])) == 4:
        break
    i += 1

result = i + 4
print(f"Part 1: {result}")

# Part 2
i = 0
while i < len(data):
    if len(set(data[i : i + 14])) == 14:
        break
    i += 1

result = i + 14
print(f"Part 2: {result}")
