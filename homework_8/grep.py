#!/usr/bin/env python3

import argparse
import sys
import re
import os


parser = argparse.ArgumentParser()
parser.add_argument("regex")
parser.add_argument("files", nargs="*")
args = parser.parse_args()

pattern = re.compile(args.regex)

if len(args.files) == 0: # reading from stdin
    for line in sys.stdin:
        if pattern.search(line):
            sys.stdout.write(line)

elif len(args.files) == 1: # reading from one input file, only return lines with match
    if not os.path.isfile(args.files[0]):
        sys.stderr.write(f'grep.py: {args.files[0]}: No such file or directory\n')
        sys.exit()

    file = open(args.files[0], 'r')
    for line in file:
        if pattern.search(line):
            sys.stdout.write(line)

else: # reading from several input files, return lines with match after file name
    for document in args.files:
        if not os.path.isfile(document):
            sys.stderr.write(f'grep.py: {document}: No such file or directory\n')
            continue
        file = open(document, 'r')
        for line in file:
            if pattern.search(line):
                sys.stdout.write(f'{document}:{line}')
