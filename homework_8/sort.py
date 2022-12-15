#! /usr/bin/env python3

import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('file', nargs="*")

args = parser.parse_args()

all_lines = list()

if len(args.file) == 0:
    for line in sys.stdin:
        all_lines.append(line.strip())
else:
    for file in args.file:
        with open(file, 'r') as inp:
            for line in inp.readlines():
                all_lines.append(line.strip())

for line in sorted(sorted(all_lines), key=lambda x: x.lstrip("_").lower()):
    line = f'{line}\n'
    sys.stdout.write(line)
