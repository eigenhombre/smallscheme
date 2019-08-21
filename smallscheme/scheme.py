#!/usr/bin/env python

import re
import operator
from functools import reduce

def remove_nil_keys(m):
    for k, v in m.items():
        if v is not None:
            return k, v

pat = ("(?ms)^\s*\((?P<list>.*)\)$"
       "|"
       "(?P<bool>(\#t|\#f))\s*"
       "|"
       "(?P<atom>[a-zA-Z\+\-\*\/]+[a-zA-Z0-9\+\-\*\/]*)\s*"
       "|"
       "(?P<num>[0-9]+)\s*")

def parse_list_body(body_str):
    ret = []
    while body_str:
        m, remaining = reduce1(body_str)
        ret.append(m)
        if not remaining:
            break
        body_str = remaining
    return ret

def reduce1(x):
    match = re.search(pat, x)
    assert match, "Invalid input '%s'!" % x
    k, v = remove_nil_keys(re.search(pat, x).groupdict())
    if k == 'num':
        v = int(v)
    if k == 'bool':
        v = True if v == "#t" else False
    if k == 'list':
        v = parse_list_body(v)
    remaining = x[match.end():]
    return (k, v), remaining

def parse_str(x):
    return reduce1(x)[0]

def plus(args):
    return ('num', sum(x for (_, x) in args))

def times(args):
    return ('num', reduce(operator.mul,
                          (x for (_, x) in args),
                          1))

def minus(args):
    return ('num', args[0][1] - sum(x for (_, x) in args[1:]))

def dispatch(fn_name, args):
    fn = {'+': plus,
          '*': times,
          '-': minus}.get(fn_name, None)
    if fn is None:
        raise Exception('Unknown function name: "%s"'
                        % fn_name)
    return fn(args)

def evalu(ast):
    k, v = ast
    if k == 'num' or k == 'bool':
        return ast
    if k == 'atom' and v == '+':
        return ('intproc', '+')
    if k == 'list':
        if not v:
            return ('list', [])
        elif v[0] == ('atom', 'quote'):
            return v[1]
        else:
            (_, fn_name) = v[0]
            return dispatch(fn_name, [evalu(x) for x in v[1:]])
    raise Exception('evaluation error: "%s"' % str(ast))

def printable_value(ast):
    k, v = ast
    if k == 'num':
        return str(v)
    if k == 'bool':
        return {True: "#t",
                False: "#f"}.get(v)
    if k == 'intproc':
        return "Internal procedure '%s'" % v
    if k == 'atom':
        return v
    if k == 'list':
        return '(' + ' '.join([printable_value(x)
                                for x in v]) + ')'
    raise Exception('Unprintable ast "%s"' % ast)

def repl():
    while True:
        try:
            x = input("scheme> ").strip()
        except EOFError:
            print()
            break
        if x:
            print(printable_value(evalu(parse_str(x))))

if __name__ == "__main__":
    repl()
