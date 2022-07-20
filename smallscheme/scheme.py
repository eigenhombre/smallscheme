import lark
import operator
import random
import re
import sys
from functools import reduce

parser = lark.Lark(
    '''
start  : _exprs
_exprs : _e* _e
_e     : ATOM
       | _num
       | BOOL
       | list
TRUE   : "#t"
FALSE  : "#f"
BOOL   : TRUE | FALSE
list   : "(" _exprs? ")"
INT    : /[-+]?[0-9]+/
ATOM   : /[a-zA-Z]+[a-zA-Z0-9\-\?]*/
       | /[\*\/\=\>\<]/
       | /[\-\+](?![0-9])/
FLOAT  : /[-+]?[0-9]+\.[0-9]*/
_num   : INT | FLOAT
COMMENT : ";" /(.)*/ NEWLINE?

%import common.WS
%import common.NEWLINE
%ignore WS
%ignore COMMENT
    ''')

def atom(x):
    return 'atom', x

def list_(x):
    return 'list', x

def bool_(x):
    return 'bool', x

def int_(x):
    return 'int', x

def float_(x):
    return 'float', x

def typ(x):
    return x[0]

noop = 'nop', None

def convert_ast(ast):
    """
    Re-cast the Lark representation of the parse tree into our own.

    'start' is always the top of the tree and `convert_ast` returns a
    list of zero or more parsed expressions.

    All other entrypoints are recursively converted into the
    appropriate atom, list, int, float etc.
    """
    if type(ast) is lark.tree.Tree:
        if ast.data == "start":
            return [convert_ast(x) for x in ast.children]
        if ast.data == "list":
            return list_([convert_ast(x) for x in ast.children])
    if type(ast) is lark.lexer.Token:
        ty = ast.type.lower()
        if ty == "int":
            return int_(int(ast.value))
        if ty == "float":
            return float_(float(ast.value))
        elif ty == "bool":
            return bool_(True if ast.value == "#t" else False)
        elif ty == "atom":
            return atom(ast.value)
    raise Exception("Unparsed AST: '%s'" % ast)

def parse_str(x):
    return convert_ast(parser.parse(x))

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

def do_as_test(args):
    """
    For now, the `test` expression is simply a `progn` / `do`:
    evaluate all the arguments and return the last one.  This
    may change as the test framework gets more features.
    """
    if args:
        return args[-1]

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
                  'test': do_as_test}

def intern(env, atom_name, item):
    env[atom_name] = item

def apply(fn_form, args, env):
    (maybe_fn, (fn_name, arg_names, body)) = fn_form
    if maybe_fn != 'fn':
        raise Exception('Malformed function definition "%s"!'
                        % env[fn_name])
    # THIS IS WRONG. If env changes....
    new_env = env.copy()
    for i, x in enumerate(arg_names):
        intern(new_env, x[1], args[i])
    ret = None
    for form in body:
        ret = evalu(form, new_env)
    return ret  # Last result is returned

def truthy(x):
    return x != ('bool', False)

def eval_atom(atom_name, env):
    if atom_name in dispatch_table.keys():
        return ('intproc', atom_name)
    elif atom_name in env:
        return env[atom_name]
    else:
        raise Exception("Unbound atom '%s'!" % atom_name)

def intern_fn(env, fn_name, args, body):
    lambd = ('fn', (fn_name, args, body))
    intern(env, fn_name, lambd)

def eval_list(l, env):
    # Empty list:
    if not l:
        return list_([])
    car = l[0]
    # Special forms:
    if car == atom('quote'):
        return l[1]
    elif car == atom('cond'):
        clauses = l[1:]
        for clause in clauses:
            (maybe_list, clauselist) = clause
            if maybe_list != 'list':
                raise Exception('Cond clause "%s" not a list!"' %
                                l[1:])
            pred = clauselist[0]
            if (pred == ('atom', 'else') or
                evalu(pred, env) != bool_(False)):
                return evalu(clauselist[1], env)
        return bool_(True)
    # FIXME: cond should macroexpand to if or vice-versa?
    elif car == atom('if'):
        pred = l[1]
        if truthy(evalu(pred, env)):
            return evalu(l[2], env)
        else:
            return evalu(l[3], env)
    elif car == atom('define'):
        typ, val = l[1]
        if typ == 'atom':
            intern(env, val, evalu(l[2], env))
            return noop
        elif typ == 'list':
            (_, fn_name), args = val[0], val[1:]
            intern_fn(env, fn_name, args, l[2:])
            return noop
        else:
            raise Exception("Don't know how to bind '%s'!" % typ)
    elif car == atom('lambda'):
        typ, val = l[1]
        assert typ == 'list'
        args = val[1:]
        return ('fn', ('lambda', args, l[2:]))
    elif car == atom('or'):
        for arg in l[1:]:
            ev = evalu(arg, env)
            if truthy(ev):
                return ev
        return bool_(False)
    elif car == atom('and'):
        ev = None
        for arg in l[1:]:
            ev = evalu(arg, env)
            if not truthy(ev):
                return bool_(False)
        if ev is None:
            return bool_(True)
        else:
            return ev
    else:
        # Normal function application:
        args_evaled = [evalu(x, env) for x in l[1:]]
        # HOF:
        cartype, carval = car
        if cartype == 'list':
            hof = evalu(l[0], env)
            return apply(hof, args_evaled, env)
        # Internally-supplied functions:
        fn = dispatch_table.get(carval, None)
        if fn:
            return fn(args_evaled)
        # User-defined functions:
        if carval in env:
            return apply(env[carval], args_evaled, env)
        raise Exception('Unknown function name: "%s"'
                        % carval)

def evalu(ast, env):
    k, v = ast
    if k == 'int' or k == 'float' or k == 'bool':
        return ast
    if k == 'atom':
        return eval_atom(v, env)
    if k == 'list':
        return eval_list(v, env)
    raise Exception('evaluation error: "%s"' % str(ast))

def printable_value(ast):
    k, v = ast
    if k == 'int' or k == 'float':
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
    if k == 'nop':
        return ''
    if k == 'fn':
        (fn_name, _, _) = v
        if fn_name == 'lambda':
            return "Anonymous-function"
        return "Function-'%s'" % str(fn_name)
    raise Exception('Unprintable ast "%s"' % str(ast))

def inp():
    if sys.version_info > (2, 9):
        return input("scheme> ")
    else:
        return raw_input("scheme> ")

def repl():
    env = {}
    while True:
        try:
            x = inp().strip()
        except EOFError:
            print()
            break
        if x:
            try:
                for parsed in parse_str(x):
                    pv = printable_value(evalu(parsed, env))
                    if pv:
                        print(pv)
            except Exception as e:
                print(e)
