#!/usr/bin/env python

import sys
from scheme import evalu, repl

def run_file(filename):
    env = {}
    with open(filename) as f:
        txt = f.read()
    for p in parse_str(txt):
        evalu(p, env)

def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()

if __name__ == "__main__":
    main()
