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
    args = parser.parse_args()
    files = vars(args).get('files')
    if len(files) > 0:
        for f in files:
            run_file(f)
    else:
        repl()

if __name__ == "__main__":
    main()
