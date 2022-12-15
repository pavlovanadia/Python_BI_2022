#!/usr/bin/env python3

import argparse
import os
import sys
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("where_from", nargs="*")
parser.add_argument("where_to")
args = parser.parse_args()

if len(args.where_from) == 0:
    sys.stderr.write(f'mv.py: missing destination file operand after {args.where_to}\n')
    sys.exit()
elif not os.path.isdir(args.where_to) and len(args.where_from) > 1:
    sys.stderr.write(f'mv.py: {args.where_to} is not a directory\n')
    sys.exit()
elif len(args.where_from) == 1:
    if not os.path.exists(args.where_from[0]):
        sys.stderr.write(f'mv.py: cannot stat {args.where_from[0]}: No such file or directory\n')
        sys.exit()
    shutil.move(args.where_from[0], args.where_to)
elif os.path.isdir(args.where_to) and len(args.where_from) > 1:
    for file in args.where_from:
        if not os.path.exists(file):
            sys.stderr.write(f'mv.py: cannot stat {file}: No such file or directory\n')
            sys.exit()
        shutil.move(file, args.where_to)
