import cmath
import copy
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day23_{sys.argv[1]}_input.txt" if test_mode else f"day23_input.txt"
data = utils.input_as_lines(input_file)


def draw_elves(elf_positions):
    min_x = int(min((p.real for p in elf_positions)))
    min_y = int(min((p.imag for p in elf_positions)))
    max_x = int(max((p.real for p in elf_positions)))
    max_y = int(max((p.imag for p in elf_positions)))
    for j in range(min_y, max_y + 1):
        for i in range(min_x, max_x + 1):
            if complex(i, j) in elf_positions:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


elf_positions = set()

for j, line in enumerate(data):
    for i, c in enumerate(line):
        if c == "#":
            elf_positions.add(complex(i, j))

part2_elf_positions = copy.deepcopy(elf_positions)
# print(elf_positions)
# draw_elves(elf_positions)

rules = [
    (complex(-1, -1), complex(0, -1), complex(1, -1)),
    (complex(-1, 1), complex(0, 1), complex(1, 1)),
    (complex(-1, -1), complex(-1, 0), complex(-1, 1)),
    (complex(1, -1), complex(1, 0), complex(1, 1)),
]

for round in range(10):
    proposed_moves = {}
    for pos in elf_positions:
        surrounding_positions = set(
            (
                pos + p2
                for p2 in [
                    complex(-1, -1),
                    complex(0, -1),
                    complex(1, -1),
                    complex(-1, 0),
                    complex(1, 0),
                    complex(-1, 1),
                    complex(0, 1),
                    complex(1, 1),
                ]
            )
        )
        if surrounding_positions & elf_positions:
            new_position = None
            k = 0
            while new_position is None and k < len(rules):
                rule = rules[(round + k) % len(rules)]
                rule_positions = [pos + p2 for p2 in rule]
                if not any((r in elf_positions for r in rule_positions)):
                    new_position = rule_positions[1]
                    break

                k += 1
            if new_position:
                proposed_moves[pos] = new_position

    for current, new in proposed_moves.items():
        if len([v2 for v2 in proposed_moves.values() if v2 == new]) == 1:
            elf_positions.remove(current)
            elf_positions.add(new)

    # print(elf_positions)
    # draw_elves(elf_positions)

empty_tile_count = 0

min_x = int(min((p.real for p in elf_positions)))
min_y = int(min((p.imag for p in elf_positions)))
max_x = int(max((p.real for p in elf_positions)))
max_y = int(max((p.imag for p in elf_positions)))
for j in range(min_y, max_y + 1):
    for i in range(min_x, max_x + 1):
        if complex(i, j) not in elf_positions:
            empty_tile_count += 1

print("Part 1:", empty_tile_count)

# Part 2
elf_positions = part2_elf_positions
for round in range(0, 100000):
    proposed_moves = {}
    for pos in elf_positions:
        surrounding_positions = set(
            (
                pos + p2
                for p2 in [
                    complex(-1, -1),
                    complex(0, -1),
                    complex(1, -1),
                    complex(-1, 0),
                    complex(1, 0),
                    complex(-1, 1),
                    complex(0, 1),
                    complex(1, 1),
                ]
            )
        )
        if surrounding_positions & elf_positions:
            new_position = None
            k = 0
            while new_position is None and k < len(rules):
                rule = rules[(round + k) % len(rules)]
                rule_positions = [pos + p2 for p2 in rule]
                if not any((r in elf_positions for r in rule_positions)):
                    new_position = rule_positions[1]
                    break

                k += 1
            if new_position is not None:
                proposed_moves[pos] = new_position

    elves_moved = 0
    for current, new in proposed_moves.items():
        if len([v2 for v2 in proposed_moves.values() if v2 == new]) == 1:
            elf_positions.remove(current)
            elf_positions.add(new)
            elves_moved += 1

    if round % 100 == 0 or round > 1000:
        print(f"After {round} rounds, {elves_moved} elves moved")
        draw_elves(elf_positions)

    if elves_moved == 0:
        draw_elves(elf_positions)
        print("Part 2:", round + 1)
        break
