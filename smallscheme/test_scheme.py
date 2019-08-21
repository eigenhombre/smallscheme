#!/usr/bin/env python

import re

def remove_nil_keys(m):
    return dict((k, v) for k, v in m.items() if v is not None)

pat = ("^\s*\((?P<list>.*)\)$"
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
    elif m.get("list"):
        m["list"] = parse_list_body(m["list"])
    remaining = x[match.end():]
    return m, remaining

def read_str(x):
    return reduce1(x)[0]

def test_read_str():
    assert (read_str("x") == {'atom': 'x'})
    assert (read_str("y") == {'atom': 'y'})
    assert (read_str("yxyz") == {'atom': 'yxyz'})
    assert (read_str("1234") == {'num': 1234})
    assert (read_str("(a)") == {'list': [{'atom': 'a'}]})
    assert (read_str("(a 1 1)")
            ==
            {'list': [{'atom': 'a'}, {'num': 1}, {'num': 1}]})
    assert (read_str("(+ 2 3)")
            ==
            {'list': [{'atom': '+'}, {'num': 2}, {'num': 3}]})
    assert (read_str("(a 1 (b foo x3))")
            ==
            {'list': [{'atom': 'a'},
                      {'num': 1},
                      {'list': [{'atom': 'b'},
                                {'atom': 'foo'},
                                {'atom': 'x3'}]}]})
