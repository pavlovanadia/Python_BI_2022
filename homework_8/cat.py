#! /usr/bin/env python3

import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('file', nargs="*")

args = parser.parse_args()

if len(args.file) == 0:
    for line in sys.stdin:
        sys.stdout.write(line)
else:
    for file in args.file:
        with open(file, 'r') as inp:
            for line in inp.readlines():
                sys.stdout.write(line)
