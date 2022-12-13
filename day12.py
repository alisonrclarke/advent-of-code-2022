from collections import OrderedDict
import copy
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day12_test_input.txt" if test_mode else f"day12_input.txt"
data = utils.input_as_lines(input_file)

map_rows = []  # Elevations. Coords (i, j) are at map_rows[j][i]
start = None
end = None

for j, line in enumerate(data):
    map_rows.append([])
    for i, s in enumerate(line):
        if s == "S":
            start = (i, j)
            map_rows[j].append(0)
        elif s == "E":
            end = (i, j)
            map_rows[j].append(25)
        else:
            map_rows[j].append(ord(s) - ord("a"))


def bfs(start, parents):
    current_pos = start
    queue = [start]
    explored = [start]

    while queue:
        current_pos = queue.pop(0)
        if current_pos == end:
            return

        i, j = current_pos
        current_val = map_rows[j][i]
        choices = []
        if i > 0 and map_rows[j][i - 1] <= current_val + 1:  # left
            choices.append((i - 1, j))
        if i < len(map_rows[j]) - 1 and map_rows[j][i + 1] <= current_val + 1:  # right
            choices.append((i + 1, j))
        if j > 0 and map_rows[j - 1][i] <= current_val + 1:  # up
            choices.append((i, j - 1))
        if j < len(map_rows) - 1 and map_rows[j + 1][i] <= current_val + 1:  # down
            choices.append((i, j + 1))

        for choice in choices:
            if choice not in explored:
                explored.append(choice)
                parents[choice] = current_pos
                queue.append(choice)


parents = {}
bfs(start, parents)
print(parents)

current_pos = end
path_length = 0
while current_pos != start:
    if current_pos in parents:
        path_length += 1
        current_pos = parents[current_pos]
    else:
        break

print(f"Part 1: {path_length}")

# Part 2
all_start_positions = [
    (i, j)
    for j, row in enumerate(map_rows)
    for i, val in enumerate(map_rows[j])
    if val == 0
]
min_path_length = path_length

for start in all_start_positions:
    parents = {}
    bfs(start, parents)
    current_pos = end
    path_length = 0
    success = True
    while current_pos != start:
        if current_pos in parents:
            path_length += 1
            current_pos = parents[current_pos]
        else:
            success = False
            break
    if success:
        print("Got path from ", start, ", length ", path_length)
        min_path_length = min(path_length, min_path_length)

print(f"Part 2: {min_path_length}")
