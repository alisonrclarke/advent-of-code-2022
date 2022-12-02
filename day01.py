import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day01_test_input.txt" if test_mode else f"day01_input.txt"
data = utils.input_as_lines(input_file)
data.append("")  # Add new line at end to make sure we count the last sections

# Part 1
max_calories = 0
current_calories = 0

for line in data:
    if line == "":
        if current_calories > max_calories:
            max_calories = current_calories
        current_calories = 0
    else:
        current_calories += int(line)

print(f"Part 1: {max_calories}")


# Part 2
max_calories = [0, 0, 0]  # Will be kept in descending order
current_calories = 0

for line in data:
    if line == "":
        if current_calories > max_calories[2]:
            max_calories[2] = current_calories
            max_calories.sort(reverse=True)
        current_calories = 0
    else:
        current_calories += int(line)

print(f"Part 2: {sum(max_calories, 0)}")
