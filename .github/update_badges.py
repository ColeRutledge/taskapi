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

    subprocess.run('git config user.name github-actions'.split(), check=True)
    subprocess.run('git config user.email github-actions@github.com'.split(), check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    changes_to_commit = subprocess.run(
        args=['git', 'status', '--porcelain'],
        capture_output=True, text=True, check=True).stdout
    if changes_to_commit:
        subprocess.run(['git', 'commit', '-m', '":robot: badge update"'], check=True)
        subprocess.run(['git', 'push'], check=True)


# git config user.name github-actions
# git config user.email github-actions@github.com
# git add .
# if [[ -z $(git status --porcelain) ]]
# then
#     echo "tree is clean -> skipping"
# else
#     git commit -m ':robot: badge update'
#     git push
# fi
