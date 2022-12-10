from enum import Enum
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day09_test_input.txt" if test_mode else f"day09_input.txt"
data = utils.input_as_lines(input_file)


class Direction(Enum):
    R = (1, 0)
    L = (-1, 0)
    U = (0, 1)
    D = (0, -1)


# Part 1
h_pos = (0, 0)
t_pos = (0, 0)
all_tail_positions = set()
all_tail_positions.add(t_pos)

for line in data:
    dir, dist = line.split()
    dir = Direction[dir]
    dist = int(dist)

    for i in range(dist):
        h_pos = (h_pos[0] + dir.value[0], h_pos[1] + dir.value[1])
        dx = abs(h_pos[0] - t_pos[0])
        dy = abs(h_pos[1] - t_pos[1])

        if dx == 0 and dy > 1 or dy == 0 and dx > 1:
            # In same row or col so just move tail same way as head
            t_pos = (t_pos[0] + dir.value[0], t_pos[1] + dir.value[1])
        elif dx + dy > 2:
            # Need to move tail diagonally to catch up with head
            if dir == Direction.R or dir == Direction.L:
                # Move x in same direction, make y the same as head
                t_pos = (t_pos[0] + dir.value[0], h_pos[1])
            else:
                # Move y in same direction, make x the same as head
                t_pos = (h_pos[0], t_pos[1] + dir.value[1])

        all_tail_positions.add(t_pos)

print(f"Part 1: {len(all_tail_positions)}")

# Part 2
knots = [(0, 0) for _ in range(10)]
all_tail_positions = set()
all_tail_positions.add(knots[-1])


def print_grid(knots):
    rx = range(min(k[0] for k in knots), max(k[0] for k in knots))
    ry = range(max(k[1] for k in knots), min(k[1] for k in knots), -1)
    print(f"Grid in x {rx}, y {ry}")
    for y in ry:
        row = ""
        for x in rx:
            try:
                row += str(knots.index((x, y)))
            except:
                row += "."
        print(row)


for line in data:
    dir, dist = line.split()
    dir = Direction[dir]
    dist = int(dist)

    for i in range(dist):
        current_dir = dir.value
        for j, knot in enumerate(knots):
            if j == 0:
                knots[j] = (knots[j][0] + dir.value[0], knots[j][1] + dir.value[1])
            else:
                dx = abs(knots[j][0] - knots[j - 1][0])
                dy = abs(knots[j][1] - knots[j - 1][1])

                if dx == 0 and dy > 1:
                    # In same row so just move tail in that dir to catch up
                    knots[j] = (knots[j][0], knots[j][1] + current_dir[1])
                elif dy == 0 and dx > 1:
                    # In same col so just move tail in that dir to catch up
                    knots[j] = (knots[j][0] + current_dir[0], knots[j][1])
                else:
                    # Need to move tail diagonally to catch up with prev
                    old_pos = knots[j]
                    if dx > 1 and dy == 1:
                        # Further away in x dir than y so get in line with y and move x by 1
                        knots[j] = (knots[j][0] + current_dir[0], knots[j - 1][1])
                    elif dx == 1 and dy > 1:
                        # Further away in y dir than x so get in line with x and move y by 1
                        knots[j] = (knots[j - 1][0], knots[j][1] + current_dir[1])
                    elif dy > 1 and dx > 1:
                        # Move by current dir
                        knots[j] = (
                            knots[j][0] + current_dir[0],
                            knots[j][1] + current_dir[1],
                        )

                    current_dir = (knots[j][0] - old_pos[0], knots[j][1] - old_pos[1])

        # print(line)
        # print_grid(knots)
        all_tail_positions.add(knots[-1])

print(f"Part 2: {len(all_tail_positions)}")
