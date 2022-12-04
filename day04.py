import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day04_test_input.txt" if test_mode else f"day04_input.txt"
data = utils.input_as_lines(input_file)

# Part 1
count = 0
for line in data:
    elf1_areas, elf2_areas = [
        (int(s2[0]), int(s2[1])) for s2 in [s1.split("-") for s1 in line.split(",")]
    ]
    if (
        elf1_areas[0] >= elf2_areas[0]
        and elf1_areas[1] <= elf2_areas[1]
        or elf2_areas[0] >= elf1_areas[0]
        and elf2_areas[1] <= elf1_areas[1]
    ):
        count += 1

print(f"Part 1: {count}")

count = 0
for line in data:
    elf1_areas, elf2_areas = [
        set(range(int(s2[0]), int(s2[1]) + 1))
        for s2 in [s1.split("-") for s1 in line.split(",")]
    ]
    if len(elf1_areas & elf2_areas):
        count += 1

print(f"Part 2: {count}")
