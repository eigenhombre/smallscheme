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
    new_env = Env(fn_env)
    for nam, arg in zip(arg_names, arg_vals):
        assert typeof(nam) == 'atom'
        intern(new_env, value(nam), arg)
    results = [evalu(form, new_env) for form in body]
    return results[-1]

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

def eval_let(env, bindings, body):
    """
    `let` can be a syntactic transformation of a lambda
    expression, but we implement it directly here in this function.
    """
    new_env = Env(env)
    for ll in value(bindings):
        assert typeof(ll) == 'list', 'bindings must be a list'
        pair = value(ll)
        assert len(pair) == 2, 'bindings must be pairs'
        nam, arg = pair
        assert typeof(nam) == 'atom', 'binding LHS must be atom'
        intern(new_env, value(nam), evalu(arg, env))
    args_evaled = [evalu(x, new_env) for x in body]
    return args_evaled[-1]

def eval_cond(env, clauses):
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
    # don't have a void value (yet), but if nothing matches we
    # should return something falsey:
    return FALSE

def eval_define(env, args):
    var_or_fnpat = args[0]
    typ = typeof(var_or_fnpat)
    if typ == 'atom':
        binding_name = value(var_or_fnpat)
        intern(env, binding_name, evalu(args[1], env))
        return noop
    elif typ == 'list':
        val = value(var_or_fnpat)
        fn_name = val[0][1]
        arg_names = val[1:]
        body = args[1:]
        intern(env, fn_name, make_fn(fn_name,
                                     arg_names,
                                     body,
                                     env))
        return noop
    else:
        raise Exception("Don't know how to define '%s'!" % l[1:])

def eval_list(expr, env):
    l = value(expr)
    # Empty list:
    if not l:
        return EMPTYLIST
    car = l[0]
    # Special forms:
    if car == QUOTE:
        return l[1]
    elif car == LET:
        return eval_let(env, l[1], l[2:])
    elif car == COND:
        return eval_cond(env, l[1:])
    # Maybe `cond` should macroexpand to `if`, or vice-versa?
    elif car == IF:
        pred = l[1]
        if truthy(evalu(pred, env)):
            return evalu(l[2], env)
        else:
            return evalu(l[3], env)
    elif car == DEFINE:
        return eval_define(env, l[1:])
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
