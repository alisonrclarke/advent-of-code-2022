import cmath
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f'day17_test_input.txt' if test_mode else f'day17_input.txt'
data = utils.input_as_string(input_file)

# moves = []
# for c in data:
#     moves.append(1 if c == '>' else -1)

class Rock:

    def __init__(self, shape, top_row_number):
        self.shape = shape # complex ints of filled spaces, with bottom left 0
        self.pos = complex(2, top_row_number + 4) # bottom left position
        self.positions = set([s + self.pos for s in self.shape])
        x_positions = [s.real for s in shape]
        self.width = max(*x_positions) - min(*x_positions) + 1

    def left(self, filled_positions, top_row_number):
        can_move = self.pos.real > 0
        if can_move and self.pos.imag <= top_row_number:
            new_pos = set((p - 1 for p in self.positions))
            if filled_positions & new_pos:
                can_move = False

        if can_move:
            self.positions = set((p - 1 for p in self.positions))
            self.pos -=1

    def right(self, filled_positions, top_row_number):
        can_move = self.pos.real < 7 - self.width
        if can_move and self.pos.imag <= top_row_number:
            new_pos = set((p + 1 for p in self.positions))
            if filled_positions & new_pos:
                can_move = False

        if can_move:
            self.positions = set((p + 1 for p in self.positions))
            self.pos +=1

    def down(self, filled_positions, top_row_number):
        if self.pos.imag == 0:
            can_move = False
        else:
            can_move = True
            if self.pos.imag > top_row_number + 1:
                can_move = True
            else:
                new_pos = set((p + complex(0, -1) for p in self.positions))
                if filled_positions & new_pos:
                    can_move = False

        if can_move:
            self.positions = set((p + complex(0, -1) for p in self.positions))
            self.pos += complex(0, -1)
        else:
            # Add current pos to filled positions
            filled_positions = filled_positions | self.positions

        return can_move, filled_positions


def print_grid(filled_positions, top_row_number, rock=None):
    if rock:
        max_height = max(*[p.imag for p in rock.positions], top_row_number)
    else:
        max_height = top_row_number
    for j in range(int(max_height), -1, -1):
        line = '|'
        for i in range(7):
            if complex(i, j) in filled_positions:
                line += '#'
            elif rock and complex(i, j) in rock.positions:
                line += '@'
            else:
                line += '.'
        print(line + '|')
    print('+-------+')
    print()



rock_shapes = [
    # ####
    set((
        complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)
    )),

    # .#.
    # ###
    # .#.
    set((
        complex(1, 2),
        complex(0, 1), complex(1, 1), complex(2, 1),
        complex(1, 0)
    )),

    # ..#
    # ..#
    # ###
    set((
        complex(2, 2),
        complex(2, 1),
        0, 1, 2
    )),

    # #
    # #
    # #
    # #
    set((
        complex(0, 3),
        complex(0, 2),
        complex(0, 1),
        0
    )),

    # ##
    # ##
    set((
        complex(0, 1), complex(1, 1),
        0, 1
    )),
]

top_row_number = -1
shape_index = 0
step = 0
filled_positions = set()

for i in range(2022):
    rock = Rock(rock_shapes[shape_index % len(rock_shapes)], top_row_number)
    shape_index += 1

    while(True):
        # print_grid(filled_positions, top_row_number, rock)
        move = data[step % len(data)]
        step += 1
        if move == '<':
            rock.left(filled_positions, top_row_number)
        else:
            rock.right(filled_positions, top_row_number)

        moved, filled_positions = rock.down(filled_positions, top_row_number)
        if not moved:
            if filled_positions:
                top_row_number = max((p.imag for p in filled_positions))
            # print_grid(filled_positions, top_row_number)
            break

print(f"Part 1: {top_row_number + 1}")


# def pattern_search(pattern_rows, remaining_rows):
#     if len(remaining_rows) == 0:
#         return []
#
#     for pattern_row in pattern_rows:
#         indices = pattern_search(pattern_row, remaining_rows[1:])

def find_rows_filled(n_rocks, stop_at_height=None):
    base = 0
    top_row_number = -1
    shape_index = 0
    step = 0
    filled_positions = set()

    for i in range(n_rocks):
        rock = Rock(rock_shapes[shape_index % len(rock_shapes)], top_row_number)
        shape_index += 1

        while(True):
            # print_grid(filled_positions, top_row_number, rock)
            move = data[step % len(data)]
            step += 1
            if move == '<':
                rock.left(filled_positions, top_row_number)
            else:
                rock.right(filled_positions, top_row_number)

            moved, filled_positions = rock.down(filled_positions, top_row_number)
            if not moved:
                if filled_positions:
                    top_row_number = max((p.imag for p in filled_positions))
                # print_grid(filled_positions, top_row_number)
                break

        # Need to remove items from filled_positions once there's a continuous line across
        # This isn't enough: also look for lines up/down from current
        # Or try only doing every 10000 rows
        if i % 1000 == 0:
            # for j in range(int(top_row_number), -1, -1):
            #     found_path = True
            #     if complex(0, j) not in filled_positions:
            #         continue
            #     k = 0
            #     while found_path:
            #         if complex(k, j) not in filled_positions:
            #         if complex(k, j) not in filled_positions:
            #             full = False
            #
            #     if full:
            #         # print(f"Trimming from row {j}...")
            #         # print_grid(filled_positions, top_row_number)
            #         # Can remove everything below this row from filled_positions
            #         new_filled_positions = set()
            #         for pos in filled_positions:
            #             if pos.imag > j:
            #                 new_filled_positions.add(pos - complex(0, j))
            #         filled_positions = new_filled_positions
            #         base += top_row_number
            #         top_row_number = top_row_number - j
            #         # print_grid(filled_positions, top_row_number)

            # Alternatively: look for repeating patterns
            rows = []
            for j in range(int(top_row_number), -1, -1):
                row = [1 if complex(k, j) in filled_positions else 0 for k in range(0, 7)]
                rows.append(row)

            indices = [k for k, row in enumerate(rows) if row == rows[0]]
            found_pattern = False
            pattern_index = 0
            for j in indices[1:]:
                is_match = True
                for k, row in enumerate(rows[1:j]):
                    if len(rows) < j + k + 2 or row != rows[j+k+1]:
                        is_match = False
                        break
                if is_match:
                    print("Found repeated pattern at index", j)
                    assert rows[:j] == rows[j:j*2]
                    if len(rows) > j*3:
                        assert rows[:j] == rows[j*2:j*3]
                        print("Pattern repeats 3 times - success!")
                        found_pattern = True
                        pattern_index = j
                        break
                    else:
                        print("Waiting for more results")
            
            if found_pattern:
                # Something wrong in logic here - number of rocks dropped or n_repeats
                new_limit = n_rocks % pattern_index
                rocks_dropped_to_pattern, _ = find_rows_filled(i, stop_at_height=pattern_index)
                print("rocks dropped to pattern", rocks_dropped_to_pattern)
                n_repeats = n_rocks // rocks_dropped_to_pattern
                new_limit = n_rocks % rocks_dropped_to_pattern
                print("new limit", new_limit)
                return n_repeats * pattern_index + find_rows_filled(new_limit)

        if i % 10000 == 0:
            print(i, len(filled_positions))

        if stop_at_height and top_row_number > stop_at_height:
            return i-1, top_row_number
            
    return top_row_number + 1

rows_filled = find_rows_filled(1000000000000)

print(f"Part 2: {rows_filled}")
