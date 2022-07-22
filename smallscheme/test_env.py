from smallscheme.dtypes import *
from smallscheme.env import Env

def test_env():
    outer = Env()
    outer['a'] = int_(0)
    assert 'a' in outer
    assert 'b' not in outer
    assert outer['a'] == int_(0)

    inner = Env(outer)
    assert 'a' in inner
    assert 'b' not in inner
    assert inner['a'] == int_(0)

    inner['c'] = int_(1)
    assert 'c' in inner
    assert 'c' not in outer
    assert inner['c'] == int_(1)

    outer['d'] = int_(2)
    assert 'd' in outer
    assert 'd' in inner
    assert inner['d'] == int_(2)

    # Overriding higher-level (global) env with
    # inner scope:
    inner['a'] = int_(3)
    assert 'a' in outer
    assert 'a' in inner
    assert inner['a'] == int_(3)
    assert outer['a'] == int_(0)
