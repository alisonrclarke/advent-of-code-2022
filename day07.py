import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day07_test_input.txt" if test_mode else f"day07_input.txt"
data = utils.input_as_lines(input_file)

dir_tree = {}
cwd_path = []
cwd_tree = dir_tree


def get_tree_at_path(dir_tree, path):
    current_tree = dir_tree
    for p in path:
        current_tree = current_tree[p]
    return current_tree


for line in data:
    if line.startswith("$ cd"):
        cd_dir = line[5:]
        if cd_dir == "..":
            cwd_path.pop()
            cwd_tree = get_tree_at_path(dir_tree, cwd_path)
        else:
            cwd_path.append(cd_dir)
            if cd_dir not in cwd_tree:
                cwd_tree[cd_dir] = {}
            cwd_tree = cwd_tree[cd_dir]
    elif not line.startswith("$ ls"):
        # File or dir
        splits = line.split()
        if splits[0] == "dir":
            cwd_tree[splits[1]] = {}
        else:
            cwd_tree[splits[1]] = int(splits[0])

# Part 1
def get_size(dir_obj, current_total):
    if isinstance(dir_obj, int):
        return (dir_obj, current_total)
    else:
        size = 0
        for sub_obj in dir_obj.values():
            current_size, current_total = get_size(sub_obj, current_total)
            size += current_size

        if size <= 100000:
            current_total += size
        return (size, current_total)


dir_size, total = get_size(dir_tree, 0)
print(f"Part 1: {total}")


# Part 2
current_free_space = 70000000 - dir_size
free_space_needed = 30000000 - current_free_space


def get_size(dir_obj, current_min):
    if isinstance(dir_obj, int):
        return (dir_obj, current_min)
    else:
        size = 0
        for sub_obj in dir_obj.values():
            current_size, current_min = get_size(sub_obj, current_min)
            size += current_size

        if size >= free_space_needed and size < current_min:
            current_min = size

        return (size, current_min)


size, min_value = get_size(dir_tree, 70000000)
print(f"Part 2: {min_value}")
