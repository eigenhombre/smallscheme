#!/usr/bin/env python

import sys
import argparse
from scheme import evalu, repl, parse_str

def run_file(filename):
    env = {}
    with open(filename) as f:
        txt = f.read()
    for p in parse_str(txt):
        evalu(p, env)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files', metavar='file', type=str, nargs='*',
        help='Files to process; if none given, a REPL will start')
    parser.add_argument(
        '-t', dest='test_files', action='append',
        help='Run test file')
    args = parser.parse_args()

    test_files = vars(args).get('test_files')
    if test_files and len(test_files) > 0:
        for f in test_files:
            run_file(f)
        return

    files = vars(args).get('files')
    if files and len(files) > 0:
        for f in files:
            run_file(f)
    else:
        repl()

if __name__ == "__main__":
    main()
