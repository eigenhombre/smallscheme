import re
import sys
from smallscheme.env import Env
from smallscheme.parse import parse_str
from smallscheme.dtypes import *
from smallscheme.builtin import dispatch_table

def intern(env, atom_name, item):
    env[atom_name] = item

def apply(fn_form, args, env):
    (maybe_fn, (fn_name, arg_names, body)) = fn_form
    assert typeof(fn_form) == 'fn'
    # FIXME: store env with lambda definition, for lexical closures.
    new_env = Env(env)
    for nam, arg in zip(arg_names, args):
        assert typeof(nam) == 'atom'
        intern(new_env, value(nam), arg)
    ret = None
    for form in body:
        ret = evalu(form, new_env)
    return ret  # Last result is returned, or None if none

def truthy(x):
    return x != FALSE

def eval_atom(atom, env):
    atom_name = value(atom)
    if atom_name in dispatch_table.keys():
        return ('intproc', atom_name)
    elif atom_name in env:
        return env[atom_name]
    else:
        raise Exception("Unbound atom '%s'!" % atom_name)

def intern_fn(env, fn_name, args, body):
    lambd = ('fn', (fn_name, args, body))
    intern(env, fn_name, lambd)

def eval_list(expr, env):
    l = value(expr)
    # Empty list:
    if not l:
        return list_([])
    car = l[0]
    # Special forms:
    if car == QUOTE:
        return l[1]
    elif car == COND:
        clauses = l[1:]
        for clause in clauses:
            (maybe_list, clauselist) = clause
            if maybe_list != 'list':
                raise Exception('Cond clause "%s" not a list!"' %
                                l[1:])
            pred = clauselist[0]
            if (pred == ('atom', 'else') or
                evalu(pred, env) != FALSE):
                return evalu(clauselist[1], env)
        # Edge case: Racket with `#lang sicp` returns #<void>; we
        # don't have that, but if nothing matches we should return
        # something falsey:
        return FALSE
    # Maybe `cond` should macroexpand to `if`, or vice-versa?
    elif car == IF:
        pred = l[1]
        if truthy(evalu(pred, env)):
            return evalu(l[2], env)
        else:
            return evalu(l[3], env)
    elif car == DEFINE:
        var_or_fnpat = l[1]
        typ, val = typeof(var_or_fnpat), value(var_or_fnpat)
        if typ == 'atom':
            intern(env, val, evalu(l[2], env))
            return noop
        elif typ == 'list':
            (_, fn_name), args = typeof(val), val[1:]
            intern_fn(env, fn_name, args, l[2:])
            return noop
        else:
            raise Exception("Don't know how to bind '%s'!" % typ)
    elif car == LAMBDA:
        typ, val = l[1]
        assert typ == 'list'
        args = val[1:]
        return ('fn', ('lambda', args, l[2:]))
    elif car == OR:
        for arg in l[1:]:
            ev = evalu(arg, env)
            if truthy(ev):
                return ev
        return FALSE
    elif car == AND:
        ev = None
        for arg in l[1:]:
            ev = evalu(arg, env)
            if not truthy(ev):
                return FALSE
        if ev is None:
            return TRUE
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

def evalu(expr, env):
    if typeof(expr) in ('int', 'float', 'bool'):
        return expr
    if typeof(expr) == 'atom':
        return eval_atom(expr, env)
    if typeof(expr) == 'list':
        return eval_list(expr, env)
    raise Exception('evaluation error: "%s"' % str(expr))

def inp():
    if sys.version_info > (2, 9):
        return input("scheme> ")
    else:
        return raw_input("scheme> ")

def repl():
    env = Env()
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
