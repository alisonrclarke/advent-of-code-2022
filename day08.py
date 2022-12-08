import sys
from typing import List

import utils

test_mode = len(sys.argv) > 1
input_file = f"day08_test_input.txt" if test_mode else f"day08_input.txt"
data = utils.input_as_lines(input_file)

rows = []
for line in data:
    rows.append([int(c) for c in line])

cols = []  # Duplicate the data but will make lookups easier later
for i in range(len(rows[0])):
    cols.append([r[i] for r in rows])

# Part 1
visible_count = 0

for j, row in enumerate(rows):
    for i, h in enumerate(row):
        if (
            all([h2 < h for h2 in row[:i]])
            or all([h2 < h for h2 in row[i + 1 :]])
            or all([h2 < h for h2 in cols[i][:j]])
            or all([h2 < h for h2 in cols[i][j + 1 :]])
        ):
            visible_count += 1

print(f"Part 1: {visible_count}")

# Part 2
max_scenic_score = 0


def get_score_for_dir(h: int, tree_heights: List[int]) -> int:
    if not tree_heights:
        return 0
    score = 0
    for i in range(len(tree_heights)):
        if i == 0:
            score += 1
        elif tree_heights[i] >= tree_heights[i - 1]:
            # this tree is bigger than the previous so is visible
            score += 1
        elif (
            all([h2 < h for h2 in tree_heights[:i]])
            and tree_heights[i] <= tree_heights[i - 1]
        ):
            # this tree is smaller than the one before it and all the ones before it are smaller than h
            # so is visble as you look down
            score += 1
        else:
            break
    return score


for j, row in enumerate(rows):
    for i, h in enumerate(row):
        score = (
            get_score_for_dir(h, list(reversed(row[:i])))
            * get_score_for_dir(h, row[i + 1 :])
            * get_score_for_dir(h, list(reversed(cols[i][:j])))
            * get_score_for_dir(h, cols[i][j + 1 :])
        )
        max_scenic_score = max(score, max_scenic_score)

print(f"Part 2: {max_scenic_score}")
