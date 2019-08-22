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
            | NUM
            | BOOL
            | list
TRUE        : "#t"
FALSE       : "#f"
BOOL        : TRUE | FALSE
list        : "(" _exprs? ")"
ATOM        : /[a-zA-Z\+\*\-\/]+[a-zA-Z0-9]*/
NUM         : /[0-9]+/
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
        if ty == "num":
            return (ty, int(ast.value))
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

def plus(args):
    return ('num', sum(x for (_, x) in args))

def times(args):
    return ('num', reduce(operator.mul,
                          (x for (_, x) in args),
                          1))

def minus(args):
    return ('num', args[0][1] - sum(x for (_, x) in args[1:]))

def divide(args):
    return ('num',
            args[0][1] // reduce(operator.mul,
                                 (x for (_, x) in args[1:]),
                                 1))

def dispatch(fn_name, args):
    fn = {'+': plus,
          '*': times,
          '-': minus,
          '/': divide}.get(fn_name, None)
    if fn is None:
        raise Exception('Unknown function name: "%s"'
                        % fn_name)
    return fn(args)

def evalu(ast):
    k, v = ast
    if k == 'num' or k == 'bool':
        return ast
    if k == 'atom' and v in ['+', '-', '/', '*']:
        return ('intproc', v)
    if k == 'list':
        if not v:
            return ('list', [])
        elif v[0] == ('atom', 'quote'):
            return v[1]
        else:
            (_, fn_name) = v[0]
            return dispatch(fn_name, [evalu(x) for x in v[1:]])
    raise Exception('evaluation error: "%s"' % str(ast))

def printable_value(ast):
    k, v = ast
    if k == 'num':
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
    raise Exception('Unprintable ast "%s"' % ast)

def repl():
    while True:
        try:
            x = input("scheme> ").strip()
        except EOFError:
            print()
            break
        if x:
            print(printable_value(evalu(parse_str(x))))

if __name__ == "__main__":
    repl()
