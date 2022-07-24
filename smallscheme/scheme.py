import sys
from smallscheme.env import Env
from smallscheme.parse import parse_str
from smallscheme.dtypes import *
from smallscheme.builtin import dispatch_table

def intern(env, atom_name, item):
    env[atom_name] = item

def apply(fn_form, arg_vals):
    (maybe_fn, (fn_name, arg_names, body, fn_env)) = fn_form
    assert typeof(fn_form) == 'fn'
    # FIXME: store env with lambda definition, for lexical closures.
    new_env = Env(fn_env)
    for nam, arg in zip(arg_names, arg_vals):
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
        typ = typeof(var_or_fnpat)
        if typ == 'atom':
            binding_name = value(var_or_fnpat)
            intern(env, binding_name, evalu(l[2], env))
            return noop
        elif typ == 'list':
            val = value(var_or_fnpat)
            fn_name = val[0][1]
            arg_names = val[1:]
            body = l[2:]
            intern(env, fn_name, make_fn(fn_name,
                                         arg_names,
                                         body,
                                         env))
            return noop
        else:
            raise Exception("Don't know how to define '%s'!" % l[1:])
    elif car == LAMBDA:
        typ, val = l[1]
        assert typ == 'list'
        args = val[1:]
        body = l[2:]
        lambda_args = l[1]
        return make_fn('lambda', lambda_args[1], body, env)
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
            return apply(hof, args_evaled)
        # Internally-supplied functions:
        fn = dispatch_table.get(carval, None)
        if fn:
            return fn(args_evaled)
        # User-defined functions:
        if carval in env:
            return apply(env[carval], args_evaled)
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
