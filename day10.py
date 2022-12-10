import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day10_test_input.txt" if test_mode else f"day10_input.txt"
data = utils.input_as_lines(input_file)

# Part 1
cycle = 1
x = 1
next_sig_cycle = 20
total = 0

for line in data:
    if line.startswith("addx"):
        inc = int(line.split()[1])
        cycle_count = 2
    else:
        inc = 0
        cycle_count = 1

    if cycle <= next_sig_cycle and cycle + cycle_count > next_sig_cycle:
        total += next_sig_cycle * x
        next_sig_cycle += 40

    x += inc
    cycle += cycle_count

print(f"Part 1: {total}")

# Part 1
cycle = 1
x = 1
crt_rows = ["" for _ in range(8)]
pos = 0

for line in data:
    if line.startswith("addx"):
        inc = int(line.split()[1])
        cycle_count = 2
    else:
        inc = 0
        cycle_count = 1

    for i in range(cycle_count):
        row = pos // 40
        sprite_pos = 40 * row + x

        if pos >= sprite_pos - 1 and pos <= sprite_pos + 1:
            crt_rows[row] += "#"
        else:
            crt_rows[row] += "."

        pos += 1

    x += inc
    cycle += cycle_count

print(f"Part 2:")
for line in crt_rows:
    print(line)
