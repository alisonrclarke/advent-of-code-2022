import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f'day18_{sys.argv[1]}_input.txt' if test_mode else 'day18_input.txt'
data = utils.input_as_lines(input_file)

cubes = set()

for line in data:
    cubes.add(tuple((int(i) for i in line.split(','))))

# Part 1
surface_area = 0
for c in cubes:
    next_cubes = [
        (c[0]+1, c[1], c[2]),
        (c[0]-1, c[1], c[2]),
        (c[0], c[1]+1, c[2]),
        (c[0], c[1]-1, c[2]),
        (c[0], c[1], c[2]+1),
        (c[0], c[1], c[2]-1)
    ]
    for cube2 in next_cubes:
        if cube2 not in cubes:
            surface_area += 1

print("Part 1", surface_area)

# Part 2
surface_area = 0
open_sides = set()
for c in cubes:
    next_cubes = [
        (c[0]+1, c[1], c[2]),
        (c[0]-1, c[1], c[2]),
        (c[0], c[1]+1, c[2]),
        (c[0], c[1]-1, c[2]),
        (c[0], c[1], c[2]+1),
        (c[0], c[1], c[2]-1)
    ]
    for cube2 in next_cubes:
        if cube2 not in cubes:
            open_sides.add((c, cube2))
            surface_area += 1

droplet_mins = (
    min(*(c[0] for c in cubes)),
    min(*(c[1] for c in cubes)),
    min(*(c[2] for c in cubes)),
)
droplet_maxes = (
    max(*(c[0] for c in cubes)),
    max(*(c[1] for c in cubes)),
    max(*(c[2] for c in cubes)),
)

def has_path_to_outside(c, visited, enclosed):
    visited.add(c)
    
    if c in enclosed:
        return False

    if (
        c[0] <= min([c2[0] for c2 in cubes if c2[1] == c[1] and c2[2] == c[2]], default=1000000) or
        c[1] <= min([c2[1] for c2 in cubes if c2[0] == c[0] and c2[2] == c[2]], default=1000000) or
        c[2] <= min([c2[2] for c2 in cubes if c2[0] == c[0] and c2[1] == c[1]], default=1000000) or
        c[0] >= max([c2[0] for c2 in cubes if c2[1] == c[1] and c2[2] == c[2]], default=-1) or
        c[1] >= max([c2[1] for c2 in cubes if c2[0] == c[0] and c2[2] == c[2]], default=-1) or
        c[2] >= max([c2[2] for c2 in cubes if c2[0] == c[0] and c2[1] == c[1]], default=-1)
    ):
        # c is on outside       
        return True
    
    next_cubes = [
        (c[0]+1, c[1], c[2]),
        (c[0]-1, c[1], c[2]),
        (c[0], c[1]+1, c[2]),
        (c[0], c[1]-1, c[2]),
        (c[0], c[1], c[2]+1),
        (c[0], c[1], c[2]-1)
    ]
    
    has_path = False
    for c2 in [c3 for c3 in next_cubes if c3 not in cubes]:
        if c2 not in visited:
            has_path = has_path_to_outside(c2, visited, enclosed)
            if has_path:
                return True

    enclosed.add(c)
    return False

visited = set()
enclosed = set()

for (c1, c2) in open_sides:
    # c1 is filled, c2 is empty
    # Start search at c2 for path to outside
    has_path = has_path_to_outside(c2, visited, enclosed)
    if not has_path:
        surface_area -= 1

# Try drawing slices to see where holes are
for z in range(droplet_mins[2], droplet_maxes[2]+1):
    for y in range(droplet_mins[1], droplet_maxes[1]+1):
        for x in range(droplet_mins[0], droplet_maxes[0]+1):
            if (x, y, z) in enclosed:
                print('o', end='')
            elif (x, y, z) in cubes:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print('--------------------\n')


# Getting right answer for simple examples but too low for real example
# Is it missing some paths to the outside, so marking cubes as enclosed when they're not?
print("Part 2", surface_area)
