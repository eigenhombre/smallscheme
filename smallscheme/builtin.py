import operator
import random
import sys
from smallscheme.dtypes import *
from functools import reduce

def argstype(args):
    # FIXME: Unit test for argument types
    arglist = [x for (x, _) in args]
    argset = set(arglist)
    if argset == {'int', 'float'} or argset == {'float'}:
        return 'float'
    elif argset == {'int'}:
        return 'int'
    else:
        raise Exception("Bad numeric arg list: '%s'"
                        % arglist)

def plus(args):
    return (argstype(args),
            sum(x for (_, x) in args))

def times(args):
    return (argstype(args),
            reduce(operator.mul,
                   (x for (_, x) in args),
                   1))

def minus(args):
    if len(args) == 1:
        return argstype(args), -args[0][1]
    else:
        return (argstype(args),
                args[0][1] - sum(x for (_, x) in args[1:]))

def divide(args):
    return (argstype(args),
            args[0][1] // reduce(operator.mul,
                                 (x for (_, x) in args[1:]),
                                 1))

def equals(args):
    return bool_(operator.eq(*args))

def compare(args, oper):
    ((ty1, v1), (ty2, v2)) = args[:2]
    if ((ty1 != 'int' and ty1 != 'float') or
        (ty2 != 'int' and ty2 != 'float')):
        raise Exception("Type error, can't compare '%s' to '%s'!" %
                        (ty1, ty2))
    return bool_(oper(v1, v2))

def lessthan(args):
    return compare(args, operator.lt)

def greaterthan(args):
    return compare(args, operator.gt)

def notnot(args):
    if args[0] == bool_(False):
        return bool_(True)
    else:
        return bool_(False)

def car(x):
    typ, l = x[0]
    if typ != 'list':
        raise Exception("Can't take car of '%s'!"
                        % x)
    return l[0]

def cdr(x):
    typ, l = x[0]
    if typ != 'list':
        raise Exception("Can't take car of '%s'!"
                        % x)
    return list_(l[1:])

def cons(args):
    # 2-ary cons for now:
    (a, (type_l, l)) = args
    if type_l != 'list':
        raise Exception("Invalid cons args, '%s'!" % str(args))
    return list_([a] + l)

def remainder(args):
    ((t1, v1), (t2, v2)) = args
    if t1 != 'int':
        raise Exception("Invalid arg type, '%s'!" % t1)
    if t2 != 'int':
        raise Exception("Invalid arg type, '%s'!" % t2)
    return int_(v1 % v2)

def randint(arg):
    t, v = arg[0]
    if t != 'int':
        raise Exception("Invalid arg type, '%s'!" % t)
    return int_(random.randint(0, v - 1))

def display(arg):
    print(printable_value(arg[0]), end='')
    return noop

def newline(_):
    print()
    return noop

# System time in msec for use in benchmarking:
if(sys.version_info.major >= 3 and
   sys.version_info.minor >= 7):
    import time

    def runtime(_):
        return int(time.time_ns() / 1E6)
else:
    import datetime

    def runtime(_):
        return int(
            (datetime.datetime.utcnow() -
             datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

def is_assert(arg):
    t, v = arg[0]
    if v is False:
        raise AssertionError(f"is / assert failed: {arg}")
    return noop

def begin_aka_test(args):
    """
    For now, the `test` expression is simply a `begin` (like `progn`
    in Common Lisp or `do` in Clojure): evaluate all the arguments and
    return the last one.  This may change as the test framework gets
    more features.
    """
    if args:
        return args[-1]

def set_bang(args):
    pass

dispatch_table = {'+': plus,
                  '*': times,
                  '-': minus,
                  '/': divide,
                  '=': equals,
                  '<': lessthan,
                  '>': greaterthan,
                  'not': notnot,
                  'car': car,
                  'cdr': cdr,
                  'remainder': remainder,
                  'random': randint,
                  'cons': cons,
                  'display': display,
                  'newline': newline,
                  'runtime': runtime,
                  'is': is_assert,
                  'test': begin_aka_test,
                  'begin': begin_aka_test,
                  'set!': set_bang}
