#!/usr/bin/env python

import re
import ply.lex as lex

tokens = (
    'NUMBER',
    'ATOM',
    'LPAREN',
    'RPAREN',
    'BOOL'
    )

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ignore  = ' \t'

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

def t_NUMBER(t):
     r'\d+'
     t.value = int(t.value)
     return t

def t_ATOM(t):
    r'[a-zA-Z]+[a-zA-Z0-9]*|\+'
    return t

def t_BOOL(t):
    r'\#t|\#f'
    if t.value == '#t':
        t.value = True
    elif t.value == '#f':
        t.value = False
    else:
        raise Exception("bad bool!")
    return t

lexer = lex.lex()

def lexie(s):
    lexer.input(s)
    return [tok for tok in lexer]

def first(l):
    return l[0]

def atuple(s):
    fl = first(lexie(s))
    return fl.type, fl.value

def test_bools():
    assert atuple('#t')==('BOOL', True)
    assert atuple('#f')==('BOOL', False)

def test_atoms():
    assert atuple('123')==('NUMBER', 123)
    assert atuple('0')==('NUMBER', 0)
    assert atuple('QUOTE')==('ATOM', 'QUOTE')
    assert atuple('quote')==('ATOM', 'quote')
    assert atuple('a')==('ATOM', 'a')
    assert atuple('+')==('ATOM', '+')

def test_lex_sexpr():
    assert ([(tok.type, tok.value) for tok in lexie("(+ 1 1)")]
            ==
            [('LPAREN', '('),
             ('ATOM', '+'),
             ('NUMBER', 1),
             ('NUMBER', 1),
             ('RPAREN', ')')])
    assert ([(tok.type, tok.value) for tok in lexie("(quote z)")]
            ==
            [('LPAREN', '('),
             ('ATOM', 'quote'),
             ('ATOM', 'z'),
             ('RPAREN', ')')])

