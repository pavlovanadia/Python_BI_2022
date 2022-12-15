#!/usr/bin/env python3

import argparse
import os
import sys



parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*")
parser.add_argument("-l", "--lines", action="store_true")
parser.add_argument("-w", "--words", action="store_true")
parser.add_argument("-c", "--bytes", action="store_true")

args = parser.parse_args()

if len(args.files) == 0 or args.files[0] == "-":
    files = [sys.stdin]
else:
    files = args.files

vals = [False, False, False]
if args.lines == args.words == args.bytes == False:
    vals = [True, True, True]
if args.lines == True:
    vals[0] = True
if args.words == True:
    vals[1] = True
if args.bytes == True:
    vals[2] = True

for file in files:
    l, w, c = 0, 0, 0
    if file != sys.stdin:
        f = open(file, "r")
    else:
        f = file
    for line in f:
        l += 1
        w += len(line.split())
        c += len(line.encode("utf-8"))
    if file != sys.stdin:
        f.close()
    ans = []
    if vals[0]:
        ans.append(l)
    if vals[1]:
        ans.append(w)
    if vals[2]:
        ans.append(c)
    if file != sys.stdin:
        ans.append(file)

    if file != sys.stdin:
        print(" ".join(map(str, ans)))
    else:
        print(f'      {"       ".join(map(str, ans))}')
