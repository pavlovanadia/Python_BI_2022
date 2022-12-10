#!/usr/bin/env python3

import argparse
import sys
import os
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*")
parser.add_argument("-r", "-R", "--recursive", action="store_true")
args = parser.parse_args()

for file in args.files:
    if not os.path.exists(file):
        sys.stderr.write(f"rm.py: cannot remove '{file}': No such file or directory\n")
        continue

    is_dir = os.path.isdir(file)
    if is_dir and not args.recursive:
        sys.stderr.write(f"rm.py: cannot remove '{file}': Is a directory\n")
        continue

    elif is_dir:
        shutil.rmtree(file)
        continue

    is_file = os.path.isfile(file)
    if is_file:
        os.remove(file)
