#! /usr/bin/env python3

import argparse
import math
import os


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('drctrs', nargs="*", default=".")

args = parser.parse_args()

term_size = os.get_terminal_size().columns

all_files = list()

for drct in args.drctrs:
    if not os.path.isdir(drct):
        all_files.append(drct)

if len(all_files) > 0:
    print(*all_files, sep=" ")

for drct in args.drctrs:
    if not os.path.isdir(drct):
        continue
    else:
        all_drctrs = os.listdir(path=drct)
        all_drctrs.extend([".", ".."])
    if not args.all:
        hidden = list(filter(lambda x: x.startswith("."), all_drctrs))
        all_drctrs = list(set(all_drctrs).difference(set(hidden)))

    k = sum(len(i) for i in all_drctrs) + len(all_drctrs)
    if k < term_size:
        n = 0
        how_many = len(all_drctrs)
        if how_many == 0:
            if len(args.drctrs) > 1:
                print(drct + ":")
            print()
            continue
    else:
        n = len(max(all_drctrs, key=len)) # for ljust
        how_many = term_size // n

    res = sorted(all_drctrs, key=lambda x: x.lstrip(".").lower())
    res = list(map(lambda x: str(x).ljust(n), res))

    num_rows = math.ceil(len(all_drctrs) / how_many)

    res_mtr = [['' for _ in range(how_many)] for _ in range(num_rows)]
    counter = 0

    for i in range(how_many):
        if counter == len(res):
            break
        for j in range(num_rows):
            res_mtr[j][i] = res[counter]
            counter += 1
            if counter == len(res):
                break
    
    for i in range(len(res_mtr)):
        res_mtr[i][-1] = res_mtr[i][-1].strip()


    if len(args.drctrs) == 1:
        for i in res_mtr:
            print(*i)
    else:
        print(drct + ":")
        for i in res_mtr:
            print(*i)
