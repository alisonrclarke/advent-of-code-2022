import copy
import math
import sys
from typing import List

import utils

test_mode = len(sys.argv) > 1
input_file = f"day11_test_input.txt" if test_mode else f"day11_input.txt"
data = utils.input_as_lines(input_file)


class Monkey:

    all_monkeys: List["Monkey"] = []
    all_monkeys_lcm = 0

    def __init__(self, number: int):
        self.number = number
        self.items = []
        self.op = None
        self.op_val = 0
        self.test_divisible_by = 1
        self.monkey_if_true = 0
        self.monkey_if_false = 0
        self.inspected_item_count = 0

    def add_item(self, item: int):
        self.items.append(item)

    def play_round_part_1(self):
        while self.items:
            item = self.items.pop(0)
            worry_level = self.op(item)
            worry_level = worry_level // 3
            send_to: Monkey = Monkey.all_monkeys[self.monkey_if_false]

            if worry_level % self.test_divisible_by == 0:
                send_to = Monkey.all_monkeys[self.monkey_if_true]
            send_to.add_item(worry_level)
            self.inspected_item_count += 1

            # print(f"Monkey {self.number} got worry_level {worry_level}; sent {item} to Monkey {send_to.number}; items now {self.items}")

    def play_round_part_2(self):
        while self.items:
            item = self.items.pop(0)
            worry_level = self.op(item)
            send_to: Monkey = Monkey.all_monkeys[self.monkey_if_false]

            # Keep values small by capping at lowest common multiple of all monkeys' divisors
            if worry_level > Monkey.all_monkeys_lcm:
                worry_level = worry_level % Monkey.all_monkeys_lcm

            if worry_level % self.test_divisible_by == 0:
                send_to = Monkey.all_monkeys[self.monkey_if_true]
            send_to.add_item(worry_level)
            self.inspected_item_count += 1

            # print(f"Monkey {self.number} got worry_level {worry_level}; sent {item} to Monkey {send_to.number}; items now {self.items}")

    def __str__(self) -> str:
        return f"Monkey {self.number}: items {self.items}, op_val: {self.op_val}, tests for divisible by {self.test_divisible_by}, if t send to {self.monkey_if_true} else send to {self.monkey_if_false}, has inspected {self.inspected_item_count} items."


m = None
for line in data:
    line = line.strip()
    if line == "":
        continue
    if line.startswith("Monkey"):
        if m:
            Monkey.all_monkeys.append(m)
        m = Monkey(len(Monkey.all_monkeys))
    elif line.startswith("Starting items:"):
        item_str = line.split(" ", maxsplit=2)[2]
        m.items = [int(s) for s in item_str.split(", ")]
    elif line.startswith("Operation: new = old "):
        op_str = line[len("Operation: new = old ") :]
        op, val_str = op_str.split()
        m.op_val = None
        if val_str != "old":
            m.op_val = int(val_str)
        if op == "*":
            m.op = lambda x: x * (m.op_val if m.op_val is not None else x)
        else:
            m.op = lambda x: x + (m.op_val if m.op_val is not None else x)
    elif line.startswith("Test:"):
        m.test_divisible_by = int(line.split(" ")[-1])
    elif line.startswith("If true:"):
        m.monkey_if_true = int(line.split(" ")[-1])
    elif line.startswith("If false:"):
        m.monkey_if_false = int(line.split(" ")[-1])
    else:
        print("Unknown line: ", line)
        sys.exit(1)

# Add last monkey
if m:
    Monkey.all_monkeys.append(m)

# Keep a copy of original monkeys for part 2
original_monkeys = copy.deepcopy(Monkey.all_monkeys)

# Part 1
for i in range(20):
    for m in Monkey.all_monkeys:
        m.play_round_part_1()

sorted_monkeys = sorted(
    Monkey.all_monkeys, key=lambda m: m.inspected_item_count, reverse=True
)

monkey_business = (
    sorted_monkeys[0].inspected_item_count * sorted_monkeys[1].inspected_item_count
)
print(f"Part 1: {monkey_business}")

# Part 2
Monkey.all_monkeys = original_monkeys
Monkey.all_monkeys_lcm = math.lcm(*[m.test_divisible_by for m in Monkey.all_monkeys])

for i in range(10000):
    for j, m in enumerate(Monkey.all_monkeys):
        m.play_round_part_2()

sorted_monkeys = sorted(
    Monkey.all_monkeys, key=lambda m: m.inspected_item_count, reverse=True
)

monkey_business = (
    sorted_monkeys[0].inspected_item_count * sorted_monkeys[1].inspected_item_count
)
print(f"Part 2: {monkey_business}")
