#!/usr/bin/env python3

import argparse
import sys
import os


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--lines', default=10, required=False, type=int)
parser.add_argument('files', nargs='*', default=sys.stdin)

args = parser.parse_args()

output = []

""" For printing the output"""
def result(output):
    for line in output:
        sys.stdout.write(line)


if len(args.files) == 0:
    for line in sys.stdin:
        if len(output) == args.lines:
            output.pop(0)
        output.append(line)
    result(output)

elif len(args.files) == 1:

    if not os.path.exists(args.files[0]):
        sys.stderr.write(f"tail.py: cannot open '{args.files[0]}' for reading: No such file or directory\n")
        sys.exit()
    if not os.path.isfile(args.files[0]):
        sys.stderr.write(f"tail.py: error reading '{args.files[0]}': Is a directory\n")
        sys.exit()

    with open(args.files[0], 'r') as curr_file:
        for line in curr_file:
            if len(output) == args.lines:
                output.pop(0)
            output.append(line)
    result(output)

else:
    for file in args.files:
        
        if not os.path.exists(file):
            sys.stderr.write(f"tail.py: cannot open '{file}' for reading: No such file or directory\n")
            continue
        if not os.path.isfile(file):
            sys.stderr.write(f"tail.py: error reading '{file}': Is a directory\n")
            continue

        with open(file, 'r') as curr_file:
            output = []
            for line in curr_file:
                if len(output) == args.lines:
                    output.pop(0)
                output.append(line)
            output.insert(0, f'==> {file} <==\n')
            result(output)
            sys.stdout.write('\n')
