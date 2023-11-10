import operator
import re
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day21_test_input.txt" if test_mode else f"day21_input.txt"
data = utils.input_as_lines(input_file)

solved = {}
unsolved = {}

operator_pattern = re.compile(r"(\w+): (\w+) ([*+-/]) (\w+)")

for line in data:
    if m := operator_pattern.match(line):
        unsolved[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    elif line:
        i = line.index(":")
        solved[line[:i]] = int(line[i + 1 :])


def find_answer(monkey):
    if monkey in solved:
        return solved[monkey]

    m1, op, m2 = unsolved[monkey]
    m1_val = find_answer(m1)
    m2_val = find_answer(m2)

    if op == "+":
        return m1_val + m2_val
    elif op == "-":
        return m1_val - m2_val
    elif op == "*":
        return m1_val * m2_val
    elif op == "/":
        return m1_val / m2_val
    else:
        print("Aaaaaargh!")


val = find_answer("root")
print(f"Part 1: {val}")

# Part 2
solved = {}
unsolved = {}

for line in data:
    if m := operator_pattern.match(line):
        op = m.group(3)
        if m.group(1) == "root":
            op = "="
        unsolved[m.group(1)] = (m.group(2), op, m.group(4))
    elif line:
        i = line.index(":")
        if line[:i] != "humn":
            solved[line[:i]] = int(line[i + 1 :])

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}
inverse_operators = {
    "-": operator.add,
    "+": operator.sub,
    "/": operator.mul,
    "*": operator.truediv,
}


def find_answer2(monkey):
    if monkey in solved:
        return solved[monkey]
    elif monkey == "humn":
        return None

    m1, op, m2 = unsolved[monkey]
    m1_val = find_answer2(m1)
    m2_val = find_answer2(m2)

    if isinstance(m1_val, int) and isinstance(m2_val, int):
        return int(operators[op](m1_val, m2_val))
    else:
        # Can't solve, so keep track of operators on each side
        return (m1_val, op, m2_val)


def reduce(v1, op, v2):
    print("Reducing", v1, op, v2)
    if v1 is None or v2 is None:
        return (v1, op, v2)

    print(op)

    left = v1 if isinstance(v1, int) else reduce(*v1)
    right = v2 if isinstance(v2, int) else reduce(*v2)
    if isinstance(left, int) and isinstance(right, int):
        return int(operators[op](left, right))
    else:
        return (left, op, right)


def solve(v1, op, v2, ans):
    print("Solving", v1, op, v2)
    print("Answer", ans)
    if v1 is None and isinstance(v2, int):
        return int(inverse_operators[op](ans, v2))
    elif v2 is None and isinstance(v1, int):
        return int(inverse_operators[op](ans, v1))

    if isinstance(v1, int):
        # FIXME: can't just swap order for / or - !
        # Test with smaller equations
        return solve(v2[0], v2[1], v2[2], inverse_operators[op](ans, v1))
    elif isinstance(v2, int):
        return solve(v1[0], v1[1], v1[2], inverse_operators[op](ans, v2))
    else:
        breakpoint()


val = find_answer2("root")
print(val)
left = val[0] if isinstance(val[0], int) else reduce(*val[0])
right = val[2] if isinstance(val[2], int) else reduce(*val[2])

if isinstance(val[0], int):
    solved = solve(val[2][0], val[2][1], val[2][2], val[0])
else:
    solved = solve(val[0][0], val[0][1], val[0][2], val[2])
print(f"Part 2: {solved}")
