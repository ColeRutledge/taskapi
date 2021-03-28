#! /usr/bin/env python3
from pathlib import Path
import subprocess
import re


def determine_color(percentage: int):
    if percentage >= 95:
        return 'brightgreen'
    elif percentage >= 75:
        return 'yellow'
    else:
        return 'red'


if __name__ == '__main__':
    coverage = subprocess.run(
        args=['docker', 'exec', 'asana_fastapi', 'coverage', 'report'],
        text=True, capture_output=True)
    PERCENTAGE = coverage.stdout.split()[-1][:-1]
    COLOR = determine_color(int(PERCENTAGE))

    path_to_readme = Path() / '.github' / 'README.md'
    readme = open(path_to_readme).read()
    readme = re.sub(r'-\d+%25', f'-{PERCENTAGE}%25', readme)
    readme = re.sub(r'%25-\w+', f'%25-{COLOR}', readme)

    with open(path_to_readme, mode='w') as file:
        file.write(readme)
