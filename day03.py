import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day03_test_input.txt" if test_mode else f"day03_input.txt"
data = utils.input_as_lines(input_file)


def get_priority(c):
    p = ord(c)
    if ord(c) > 96:
        return p - ord("a") + 1
    else:
        return p - ord("A") + 27


# Part 1
total = 0
for line in data:
    part1 = set(line[: int(len(line) / 2)])
    part2 = set(line[int(len(line) / 2) :])
    repeated = part1.intersection(part2)
    total += get_priority(next(iter(repeated)))

print(f"Part 1: {total}")

# Part 2
total = 0
i = 0
while i < len(data):
    lines = data[i : i + 3]
    repeated = set.intersection(*[set(l) for l in lines])
    total += get_priority(next(iter(repeated)))
    i += 3

print(f"Part 2: {total}")
