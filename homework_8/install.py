#!/usr/bin/env python3

import shutil
import os
import sys


install_py_dir = os.path.abspath(os.path.dirname(__file__))
script_names = [
    "cat.py",
    "grep.py",
    "ls_beau.py",
    "ls_pipe.py",
    "mv.py",
    "rm.py",
    "sort.py",
    "tail.py",
    "wc.py"
]

path_val = os.environ["PATH"]
path_dirs = path_val.split(":")
path_target = path_dirs[-1]

for func in script_names:
    src = os.path.join(install_py_dir, func)
    if not os.path.isfile(src):
        sys.stderr.write(f"Error! Cannot find {src} - tool was not installed\n")
        continue
    dst = os.path.join(path_target, func)
    shutil.copy2(src, dst)
