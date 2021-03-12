#!/usr/bin/env python3

from pathlib import Path


# print(Path.glob(''))
print(Path.cwd())
print('hello world!')
# command = "echo hello"
# result = subprocess.run(
#     command.split(' '),
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     shell=True,
#     encoding='utf-8',
# )
# print(result.stdout)
# print(result.stderr)

# subprocess.call([shutil.which('powershell'), '-c', 'echo hello'])
# subprocess.call(["powershell", "-c", "echo hello"])

# try:
#     for line in sys.stdin:
#         print(line)
# except KeyboardInterrupt:
#     print('goodbye!')

# cp = sp.run(['wsl', 'ls', '-lh', 'foo bar baz'], check=True)
# with open('subprocess.txt', 'w') as file:
#     cp = sp.run(['wsl', 'tr', '--help'], stdout=file, check=True)
#     cp = sp.run(['wsl', 'tr', 'a-z', 'A-Z'], stdin=file)
#     print(cp)


# cwd = Path.cwd()
# proc = sp.run(['wsl', 'ls', f'{cwd}'], stdout=sp.PIPE, text=True)
# print(proc.stdout)


# cp = sp.run(
#     args=['wsl', 'tr', 'a-z', 'A-Z'],
#     input='foo bar baz',
#     check=True,
#     text=True,
#     stdout=sp.PIPE,
# )
# print(cp)

# proc = sp.run(
#     args=['wsl', 'ls', '.', 'foo bar baz'],
#     # stdout=sp.PIPE,
#     # stderr=sp.DEVNULL,
#     capture_output=True,
#     text=True,
# )
# print(proc)
# print(proc.stderr)


# branch_proc = sp.Popen(
#     args=['powershell', 'git', 'branch'],
#     stdout=sp.PIPE,
#     # stderr=sp.DEVNULL,
#     universal_newlines=True,
# )
# # print(vars(branch_proc))
# print(list(branch_proc.stdout))

# for line in branch_proc.stdout:
#     print(line)


# import time

# print(time.strftime('%m-%d-%Y %H:%M:%S'))
