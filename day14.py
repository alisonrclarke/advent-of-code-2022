import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day14_test_input.txt" if test_mode else f"day14_input.txt"
data = utils.input_as_lines(input_file)

cols = [["."]]
left_col_index = 500


def print_grid(left_col_index, cols):
    print(left_col_index)
    for j in range(len(cols[0])):
        print("|" + "".join([cols[i][j] for i in range(len(cols))]) + "|")


prev_point = None
for line in data:
    points = line.split(" -> ")
    for i, point in enumerate(points):
        x, y = (int(s) for s in point.split(","))

        # Create new rows/cols
        if x - 1 <= left_col_index:
            j = left_col_index - 1
            while j >= x - 1:
                new_col = ["." for _ in range(len(cols[0]))]
                cols = [new_col] + cols
                j -= 1
            left_col_index = x - 1
        elif x - left_col_index >= len(cols):
            j = left_col_index + len(cols)
            while j <= x + 1:
                new_col = ["." for _ in range(len(cols[0]))]
                cols.append(new_col)
                j += 1
        while len(cols[0]) <= y:
            for col in cols:
                col.append(".")

        if i > 0:
            if x == prev_point[0]:
                # Draw vertical line
                min_y = min(prev_point[1], y)
                max_y = max(prev_point[1], y)
                while min_y <= max_y:
                    cols[x - left_col_index][min_y] = "#"
                    min_y += 1
            else:
                # Draw horizontal line
                min_x = min(prev_point[0], x)
                max_x = max(prev_point[0], x)
                while min_x <= max_x:
                    cols[min_x - left_col_index][y] = "#"
                    min_x += 1

        prev_point = (x, y)

print_grid(left_col_index, cols)

y = 0
sand_count = 0
while y <= len(cols[0]):
    x = 500 - left_col_index
    y = 0
    while y < len(cols[0]) - 1:
        if cols[x][y + 1] == ".":
            pass
        elif cols[x - 1][y + 1] == ".":
            x -= 1
        elif cols[x + 1][y + 1] == ".":
            x += 1
        else:
            # Can't go any further - mark sand here
            cols[x][y] = "o"
            sand_count += 1
            break

        y += 1

    if y == len(cols[0]) - 1:  # At bottom
        break

print_grid(left_col_index, cols)

print(f"Part 1: {sand_count}")


# Part 2

# Add air then rock to bottom of cols
for col in cols:
    col.extend([".", "#"])

y = 0
at_top = False
while y < len(cols[0]):
    x = 500
    y = 0
    while y < len(cols[0]) - 1:
        # Add extra columns if x is at edge
        # Create new rows/cols
        if x - 1 < left_col_index:
            j = left_col_index - 1
            while j >= x - 1:
                new_col = ["." for _ in range(len(cols[0]))]
                new_col[-1] = "#"
                cols = [new_col] + cols
                j -= 1
            left_col_index = x - 1
        elif x - left_col_index >= len(cols) - 1:
            j = left_col_index + len(cols)
            while j <= x + 1:
                new_col = ["." for _ in range(len(cols[0]))]
                new_col[-1] = "#"
                cols.append(new_col)
                j += 1

        if cols[x - left_col_index][y + 1] == ".":
            pass
        elif cols[x - left_col_index - 1][y + 1] == ".":
            x -= 1
        elif cols[x - left_col_index + 1][y + 1] == ".":
            x += 1
        else:
            # Can't go any further - mark sand here
            cols[x - left_col_index][y] = "o"
            if y == 0:
                at_top = True
            sand_count += 1
            break

        y += 1

    if at_top:
        break

print_grid(left_col_index, cols)

print(f"Part 2: {sand_count}")
