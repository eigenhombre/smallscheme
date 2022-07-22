import re
import sys
from smallscheme.parse import parse_str
from smallscheme.dtypes import *
from smallscheme.builtin import dispatch_table

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
