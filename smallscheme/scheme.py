#!/usr/bin/env python

import re

def remove_nil_keys(m):
    return dict((k, v) for k, v in m.items()
                if v is not None)

pat = ("^\s*\((?P<list>.*)\)$"
       "|"
       "(?P<bool>(\#t|\#f))\s*"
       "|"
       "(?P<atom>[a-zA-Z\+\-\*\/]+[a-zA-Z0-9\+\-\*\/]*)\s*"
       "|"
       "(?P<num>[0-9]+)\s*")

def parse_list_body(a):
    ret = []
    while True:
        m, remaining = reduce1(a)
        ret.append(m)
        if not remaining:
            break
        a = remaining
    return ret

def reduce1(x):
    match = re.search(pat, x)
    assert match, "Invalid input '%s'!" % x
    m =  remove_nil_keys(re.search(pat, x).groupdict())
    if m.get("num"):
        m["num"] = int(m["num"])
    if m.get("bool"):
        m["bool"] = True if m["bool"] == "#t" else False
    elif m.get("list"):
        m["list"] = parse_list_body(m["list"])
    remaining = x[match.end():]
    return m, remaining

def parse_str(x):
    return reduce1(x)[0]

def evalu(ast):
    if 'num' in ast or 'bool' in ast:
        return ast
    if 'atom' in ast and ast['atom'] == "+":
        return {"intproc": "+"}
    raise Exception('evaluation error: "%s"' % ast)

def printable_value(ast):
    if 'num' in ast:
        return ast['num']
    if 'bool' in ast:
        return {True: "#t",
                False: "#f"}.get(ast['bool'])
    if 'intproc' in ast:
        return "Internal procedure '%s'" % ast['intproc']
    return ast

def repl():
    while True:
        try:
            x = input("scheme> ").strip()
        except EOFError:
            print()
            break
        if x:
            parsed = parse_str(x)
            print(parsed)
            evaluated = evalu(parsed)
            print(evaluated)
            output = printable_value(evaluated)
            print(output)

if __name__ == "__main__":
    repl()
