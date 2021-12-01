import os
import sys

day = int(sys.argv[1])

python_file = f'day{day:02}.py'
if os.path.exists(python_file):
    print(f"File {python_file} exists")
    sys.exit(1)

with open(python_file, 'w') as f:
    f.write(f"""import sys

import utils

test_mode = len(sys.argv) > 1
input_file = f'day{day:02}_test_input.txt' if test_mode else f'day{day:02}_input.txt'
data = utils.input_as_ints(input_file)
""")

open(f'day{day:02}_input.txt', 'w').close()
open(f'day{day:02}_test_input.txt', 'w').close()
