#! /usr/bin/env python3
from pathlib import Path
import subprocess as sp
import re


def determine_color(percentage: int):
    if percentage >= 95:
        return 'brightgreen'
    elif percentage >= 75:
        return 'yellow'
    else:
        return 'red'


if __name__ == '__main__':
    coverage = sp.run(
        args='docker exec asana_fastapi coverage report'.split(),
        text=True, capture_output=True, check=True)
    PERCENTAGE = coverage.stdout.split()[-1][:-1]
    COLOR = determine_color(int(PERCENTAGE))

    path_to_readme = Path() / '.github' / 'README.md'
    readme = open(path_to_readme).read()
    readme = re.sub(r'-\d+%25', f'-{PERCENTAGE}%25', readme)
    readme = re.sub(r'%25-\w+', f'%25-{COLOR}', readme)

    with open(path_to_readme, mode='w') as file:
        file.write(readme)

    sp.run('git config user.name github-actions'.split(), check=True)
    sp.run('git config user.email github-actions@github.com'.split(), check=True)
    sp.run(['git', 'add', '.'], check=True)
    changes_to_commit = sp.run(
        args=['git', 'status', '--porcelain'],
        capture_output=True, text=True, check=True).stdout
    if changes_to_commit:
        print('found changes -> committing.')
        sp.run(['git', 'commit', '-m', '":robot: badge update"'], check=True)
        sp.run(['git', 'push'], check=True)
    else:
        print('no changes -> skipping')
