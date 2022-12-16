import re
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day16_test_input.txt" if test_mode else f"day16_input.txt"
data = utils.input_as_lines(input_file)

regexp = re.compile(
    r"^Valve ([A-Z]+) has flow rate=([\d-]+); tunnels? leads? to valves? (.*)$"
)
valve_rates = {}
valve_tunnels = {}

for line in data:
    m = regexp.match(line)
    if m:
        valve = m.group(1)
        valve_rates[valve] = int(m.group(2))
        valve_tunnels[valve] = m.group(3).split(", ")
    else:
        print("Aaaarggh!", line)

print(valve_tunnels)
print(valve_rates)

# Try DFS with time limit a bit like eg IDDFS (except we just want to return pressure relieved)
