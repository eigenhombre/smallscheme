from smallscheme.dtypes import *
from smallscheme.interop import register_fn, scheme_fn
from smallscheme.parse import parse_str
from smallscheme.scheme import evalu, printable_value
from smallscheme.builtin import plus

def evstr(s):
    return evalu(parse_str(s)[0], {})

def test_interop():
    def inc(args):
        return int_(value(args[0]) + 1)
    register_fn('inc', inc)
    assert int_(2) == evstr("(inc 1)")

def test_interop_decorator():
    @scheme_fn
    def dec(args):
        return int_(value(args[0]) - 1)
    assert int_(0) == evstr("(dec 1)")

def test_override_plus():
    def strange_plus(args):
        if all(typeof(arg) in ['float', 'int']
               for arg in args):
            return int_(sum(value(arg) for arg in args))
        elif all(typeof(arg) == 'list' for arg in args):
            ret = []
            for arg in args:
                ret += value(arg)
            return list_(ret)
        else:
            return atom("aStrangerThing")
    register_fn('+', strange_plus)

    assert int_(6) == evstr("(+ 1 2 3)")
    assert (list_([int_(1), int_(2), int_(3), int_(4)]) ==
            evstr("(+ (quote (1 2)) (quote (3 4)))"))
    assert atom("aStrangerThing") == evstr("(+ 1 (quote a))")

    # restore old function for other tests!
    register_fn('+', plus)
