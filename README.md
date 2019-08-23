smallscheme
===========

[![builds.sr.ht status](https://builds.sr.ht/~eigenhombre/smallscheme.svg)](https://builds.sr.ht/~eigenhombre/smallscheme?)

A tiny scheme written in Python to prepare for
[this class](https://www.dabeaz.com/sicp.html).

Currently, this Scheme implements everything needed to follow along in [SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs) up through page **16**.

Setup
-----

`pip install -r requirements.txt`

Tests
-----

`nosetests`

REPL
----

Use `rlwrap` if you want history and that sort of thing:

    $ rlwrap ./smallscheme/scheme.py
    scheme> (quote (1 2 3 (a b c)))
    (1 2 3 (a b c))
    scheme> (+ 1 2)
    3
    scheme> (+ (* 2 4) (+ 3 5))
    16
    scheme> (/ 16 2 2 2)
    2
    scheme> +
    Internal procedure '+'
    scheme> /
    Internal procedure '/'
    scheme> (define pi 3.14159)
    scheme> (define radius 10)
    scheme> (* pi (* radius radius))
    314.159
    scheme> (define circumference (* 2 pi radius))
    scheme> circumference
    62.8318
    scheme> (define (square x) (* x x))
    scheme> (square 10)
    100
    scheme> (square (+ 2 5))
    49
    scheme> (square (square 3))
    81
    scheme> (define (sum-of-squares x y) (+ (square x) (square y)))
    scheme> (sum-of-squares 3 4)
    25
    scheme> (define (f a) (sum-of-squares (+ a 1) (* a 2)))
    scheme> (f 5)
    136
    scheme> ^D
    $


Done
----
1. Lexing of atoms and s-expressions
1. Parsing of same
1. Eval of booleans
1. Floating point and ints
1. Eval of lists
1. Function application
1. `(define ...)` for atoms, and first steps at a scope/runtime context
1. Eval of (non-built-in) atoms
1. `(define ... )` for "procedures" (functions)
1. `+ - / * = < >`
1. `cond`, `if`, `not`.

To Do
-----
1. `and`
1. `or`
1. ... everything else ....
