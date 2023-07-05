#! /usr/bin/env python3

import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('drctrs', nargs="*", default=".")

args = parser.parse_args()

all_files = list()

for drct in args.drctrs:
    if not os.path.isdir(drct):
        all_files.append(drct)

if len(all_files) > 0:
    for i in all_files:
        print(i, end="\n")

for drct in args.drctrs:
    if not os.path.isdir(drct):
        continue
    else:
        all_drctrs = os.listdir(path=drct)
        all_drctrs.extend([".", ".."])
    if not args.all:
        hidden = list(filter(lambda x: x.startswith("."), all_drctrs))
        all_drctrs = list(set(all_drctrs).difference(set(hidden)))
    if len(args.drctrs) == 1:
        for i in sorted(all_drctrs, key=lambda x: x.lstrip(".").lower()):
            print(i, end="\n")
    else:
        print(drct + ":")
        for i in sorted(all_drctrs, key=lambda x: x.lstrip(".").lower()):
            print(i, end="\n")
            