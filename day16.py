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

# print(valve_tunnels)
# print(valve_rates)

# Try DFS with time limit a bit like eg IDDFS (except we just want to return pressure relieved)
# Need to avoid loops
def dfs(valve, current_pressure_change, time_remaining, valves_opened, current_path):
    # print(valve, current_pressure_change, time_remaining)
    if valve in current_path:
        prev_index = current_path.index(valve)
        if prev_index > 0 and current_path[prev_index-1] == current_path[-1]:
            # Been here before from same dir - don't go round in circles!
            return (current_pressure_change, valves_opened, current_path)

    current_path.append(valve)

    if time_remaining == 0:
        return (current_pressure_change, valves_opened, current_path)

    # Spend a minute opening valve if not broken
    if valve_rates[valve] > 0 and valve not in valves_opened:
        time_remaining -= 1
        valves_opened.append(valve)
        current_pressure_change += time_remaining * valve_rates[valve]
        if time_remaining == 0:
            return (current_pressure_change, valves_opened, current_path)

    best = (current_pressure_change, valves_opened, current_path)
    for next_valve in valve_tunnels[valve]:
        new_pressure_change, new_valves_opened, new_current_path = dfs(next_valve, current_pressure_change, time_remaining - 1, valves_opened.copy(), current_path.copy())
        # print("checked valve", next_valve, new_pressure_change, new_valves_opened, new_current_path)
        if new_pressure_change > current_pressure_change:
            best = (new_pressure_change, new_valves_opened, new_current_path)

    # print(valve, "best is", best)
    return best


pressure_change, valves_opened, path =  dfs("AA", 0, 30, [], [])
print(pressure_change, valves_opened, path)

# Not getting right solution on test input; not completing on real input