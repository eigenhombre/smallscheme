from smallscheme.dtypes import *
from smallscheme.interop import register_fn
from smallscheme.parse import parse_str
from smallscheme.scheme import evalu, printable_value

def test_interop():
    def inc(args):
        return int_(value(args[0]) + 1)
    register_fn('inc', inc)
    assert (int_(2) == evalu(parse_str("(inc 1)")[0],
                             {}))
