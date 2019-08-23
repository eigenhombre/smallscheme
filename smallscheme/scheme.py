#!/usr/bin/env python

import lark
import operator
import re
from functools import reduce

parser = lark.Lark(
    '''
start       : _expr
_exprs      : ( _expr _whitespace )* _expr
_expr       : ATOM
            | _num
            | BOOL
            | list
TRUE        : "#t"
FALSE       : "#f"
BOOL        : TRUE | FALSE
list        : "(" _exprs? ")"
ATOM        : /[a-zA-Z\+\*\-\/\=\>\<]+[a-zA-Z0-9]*/
INT         : /[0-9]+/
FLOAT       : /[0-9]+\.[0-9]*/
_num        : INT | FLOAT
_whitespace : (" " | /\t/ )+
    ''')

def convert_ast(ast):
    if type(ast) is lark.tree.Tree:
        if ast.data == "start":
            return convert_ast(ast.children[0])
        if ast.data == "list":
            return ('list', [convert_ast(x) for x in ast.children])
    if type(ast) is lark.lexer.Token:
        ty = ast.type.lower()
        if ty == "int":
            return (ty, int(ast.value))
        if ty == "float":
            return (ty, float(ast.value))
        elif ty == "bool":
            return (ty, True if ast.value == "#t" else False)
        else:
            return (ast.type.lower(), ast.value)
    raise Exception("Unparsed AST: '%s'" % ast)

def remove_nil_keys(m):
    for k, v in m.items():
        if v is not None:
            return k, v

def parse_str(x):
    # A bit of a hack, maybe handle newlines directly in parser:
    return convert_ast(parser.parse(x.replace("\n", " ")))

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
    return (argstype(args),
            args[0][1] - sum(x for (_, x) in args[1:]))

def divide(args):
    return (argstype(args),
            args[0][1] // reduce(operator.mul,
                                 (x for (_, x) in args[1:]),
                                 1))

def equals(args):
    return ('bool', operator.eq(*args))

def compare(args, oper):
    ((ty1, v1), (ty2, v2)) = args[:2]
    if ((ty1 != 'int' and ty1 != 'float') or
        (ty2 != 'int' and ty2 != 'float')):
        raise Exception("Type error, can't compare '%s' to '%s'!" %
                        (ty1, ty2))
    return ('bool', oper(v1, v2))

def lessthan(args):
    return compare(args, operator.lt)

def greaterthan(args):
    return compare(args, operator.gt)

dispatch_table = {'+': plus,
                  '*': times,
                  '-': minus,
                  '/': divide,
                  '=': equals,
                  '<': lessthan,
                  '>': greaterthan}

def dispatch(fn_atom, env, args):
    _, fn_name = fn_atom
    fn = dispatch_table.get(fn_name, None)
    if fn is not None:
        return fn(args)
    if fn_atom in env:
        binding = env[fn_atom]
        (maybe_list,
         ((maybe_atom, maybe_lambda),
          (maybe_list, arg_names),
          rest)) = binding
        if (maybe_list != 'list' or
            maybe_atom != 'atom' or
            maybe_lambda != 'lambda'):
            raise Exception('Malformed function definition "%s"!'
                            % binding)
        new_env = env.copy()
        for i, x in enumerate(arg_names):
            new_env[x[1]] = args[i]
        return evalu(rest, new_env)
    raise Exception('Unknown function name: "%s"'
                    % fn_name)

def evalu(ast, env):
    k, v = ast
    if k == 'int' or k == 'float' or k == 'bool':
        return ast
    if k == 'atom':
        if v in dispatch_table.keys():
            return ('intproc', v)
        elif v in env:
            return env[v]
    if k == 'list':
        # Empty list:
        if not v:
            return ('list', [])
        # Special forms:
        car = v[0]
        if car == ('atom', 'quote'):
            return v[1]
        elif car == ('atom', 'define'):
            k1, v1 = v[1]
            if k1 == 'atom':
                env[v1] = evalu(v[2], env)
                return ('nop', None)
            elif k1 == 'list':
                fn_name, args = v1[0], v1[1:]
                lambd = ('list', [
                    ('atom', 'lambda'),
                    ('list', args),
                    v[2]])
                env[v1[0]] = lambd
                return ('nop', None)
            else:
                raise Exception("Don't know how to bind '%s'!" % k1)
        else:
            # Normal function application:
            return dispatch(car,
                            env,
                            [evalu(x, env) for x in v[1:]])
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
    raise Exception('Unprintable ast "%s"' % str(ast))

def repl():
    env = {}
    while True:
        try:
            x = input("scheme> ").strip()
        except EOFError:
            print()
            break
        if x:
            try:
                pv = printable_value(evalu(parse_str(x), env))
                if pv:
                    print(pv)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    repl()
