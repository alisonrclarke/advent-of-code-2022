import functools
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day13_test_input.txt" if test_mode else f"day13_input.txt"
data = utils.input_as_lines(input_file)


def is_in_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return None if left == right else left <= right
    elif isinstance(left, int):
        return is_in_order([left], right)
    elif isinstance(right, int):
        return is_in_order(left, [right])
    else:
        for j, left_item in enumerate(left):
            if j < len(right):
                right_item = right[j]
                in_order = is_in_order(left_item, right_item)
                if in_order is not None:
                    return in_order
            else:
                return False
        return True if len(left) < len(right) else None


i = 0
pair_index = 1
ordered_indices = []

while i + 1 < len(data):
    left = eval(data[i])
    right = eval(data[i + 1])
    in_order = is_in_order(left, right)
    if in_order:
        ordered_indices.append(pair_index)

    i += 3
    pair_index += 1

print(f"Part 1: {sum(ordered_indices)}")

# Part 2 - tweak sort function
def sort_fn(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return 0 if left == right else (-1 if left < right else 1)
    elif isinstance(left, int):
        return sort_fn([left], right)
    elif isinstance(right, int):
        return sort_fn(left, [right])
    else:
        for j, left_item in enumerate(left):
            if j < len(right):
                right_item = right[j]
                in_order = sort_fn(left_item, right_item)
                if in_order != 0:
                    return in_order
            else:
                return 1
        return -1 if len(left) < len(right) else 0


lines_to_sort = [eval(line) for line in data if line]
dividers = [[[2]], [[6]]]
lines_to_sort.extend(dividers)
sorted_lines = sorted(lines_to_sort, key=functools.cmp_to_key(sort_fn))

decoder_key = (sorted_lines.index(dividers[0]) + 1) * (
    sorted_lines.index(dividers[1]) + 1
)
print(f"Part 2: {decoder_key}")
