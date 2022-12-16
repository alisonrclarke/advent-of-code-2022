import cmath
import re
import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f"day15_test_input.txt" if test_mode else f"day15_input.txt"
data = utils.input_as_lines(input_file)

regexp = re.compile(
    r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)"
)
sensors = {}
beacons = set()
for line in data:
    m = regexp.match(line)
    if m:
        sensor = complex(int(m.group(1)), int(m.group(2)))
        beacon = complex(int(m.group(3)), int(m.group(4)))
        sensors[sensor] = beacon
        beacons.add(beacon)
    else:
        print("Aaaargh!")
        break

print(sensors)

min_x = int(min(*(i.real for i in sensors), *(i.real for i in beacons)))
max_x = int(max(*(i.real for i in sensors), *(i.real for i in beacons)))
max_x_dist = int(max(*((s - b).real for s, b in sensors.items())))
min_x -= max_x_dist
max_x += max_x_dist

print(min_x, max_x)

row_to_check = 10 if test_mode else 2000000

blocked_position_count = 0

# Part 1 - This is slow!!!
for x in range(min_x, max_x + 1):
    current = complex(x, row_to_check)
    if current not in beacons:
        if current in sensors:
            blocked_position_count += 1
            continue

        for s in sensors:
            sensor_to_beacon = sensors[s] - s
            sensor_beacon_dist = abs(sensor_to_beacon.real) + abs(sensor_to_beacon.imag)

            sensor_to_current = current - s
            sensor_current_dist = abs(sensor_to_current.real) + abs(
                sensor_to_current.imag
            )

            if sensor_current_dist <= sensor_beacon_dist:
                blocked_position_count += 1
                break

print(f"Day 1: {blocked_position_count}")

# Part 2 - needs optimizing!
max_coord = 20 if test_mode else 4000000

min_x = max(0, min_x)
max_x = min(max_coord, max_x)
min_y = max(
    0,
    int(
        min(
            *(
                s.imag - (abs((b - s).real) + abs((b - s).imag))
                for s, b in sensors.items()
            )
        )
    ),
)
max_y = min(
    max_coord,
    int(
        max(
            *(
                s.imag + abs((b - s).real) + abs((b - s).imag)
                for s, b in sensors.items()
            )
        )
    ),
)

sorted_sensors = sorted(list(sensors.keys()), key=lambda s: s.real)
for y in range(min_y, max_y + 1):
    x = min_x
    blocked_positions = set()
    while x < max_x + 1:
        current = complex(x, y)

        for s in sorted_sensors:
            sensor_to_beacon = sensors[s] - s
            sensor_beacon_dist = abs(sensor_to_beacon.real) + abs(sensor_to_beacon.imag)

            sensor_to_current = current - s
            sensor_current_dist = abs(sensor_to_current.real) + abs(
                sensor_to_current.imag
            )

            if s.real + sensor_beacon_dist < x:
                continue

            if sensor_current_dist <= sensor_beacon_dist:
                new_x = min(
                    int(s.real + sensor_beacon_dist - sensor_to_current.imag), max_x
                )
                blocked_positions = blocked_positions.union(range(x, new_x + 1))
                x = new_x

        x += 1

    if y % 100 == 0:
        print("row", y, "of", max_y)

    if len(blocked_positions) < (max_x - min_x) + 1:
        x = set(range(min_x, max_x + 1)).difference(blocked_positions).pop()
        print("Found", x, y)
        print("Part 2:", x * 4000000 + y)
        break
