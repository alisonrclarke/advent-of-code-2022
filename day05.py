import copy
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day05_test_input.txt" if test_mode else f"day05_input.txt"
data = utils.input_as_lines(input_file)

line_iter = iter(data)

crates = []  # List of stacks of crates, ordered from left to right then top to bottom
while line := next(line_iter, None):
    i = 0
    while i < len(line):
        crate_no = i // 4
        crate_str = line[i : i + 4]
        if crate_str.startswith("["):
            crate = crate_str[1]
            while len(crates) < crate_no + 1:
                crates.append([])
            crates[crate_no].append(crate)
        elif crate_str != "    ":
            # Reached the crate labels - break out of loop
            break
        i += 4

instructions = []
while line := next(line_iter, None):
    if line:
        instructions.append(line)

crates2 = copy.deepcopy(crates)

# Part 1
for line in instructions:
    words = line.split(" ")
    n = int(words[1])
    from_stack = int(words[3])
    to_stack = int(words[5])

    for i in range(n):
        crates[to_stack - 1].insert(0, crates[from_stack - 1].pop(0))

result = "".join([c[0] for c in crates])
print(f"Part 1: {result}")

# Part 2
for line in instructions:
    words = line.split(" ")
    n = int(words[1])
    from_stack = int(words[3])
    to_stack = int(words[5])

    crates_to_move = crates2[from_stack - 1][:n]
    crates2[from_stack - 1] = crates2[from_stack - 1][n:]
    crates2[to_stack - 1] = crates_to_move + crates2[to_stack - 1]

result = "".join([c[0] for c in crates2])
print(f"Part 2: {result}")
