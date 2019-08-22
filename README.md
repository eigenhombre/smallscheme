smallscheme
===========

[![builds.sr.ht status](https://builds.sr.ht/~eigenhombre/smallscheme.svg)](https://builds.sr.ht/~eigenhombre/smallscheme?)

A tiny scheme written in Python to prepare for
[this class](https://www.dabeaz.com/sicp.html).

Currently, this Scheme implements everything needed to follow along in [SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs) up through page **7**.

Setup
-----

`pip install -r requirements.txt`

Tests
-----

`nosetests`

REPL
----

Use `rlwrap` if you want history and that sort of thing:

    rlwrap ./smallscheme/scheme.py
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
    scheme> ^D

Done
----
1. Lexing of atoms and s-expressions
1. Parsing of same
1. Eval of booleans
1. Eval of (natural) numbers
1. Eval of lists
1. Function application
1. `(define ...)` for atoms, and first steps at a scope/runtime context
1. Eval of (non-built-in) atoms

To Do
-----
1. Boolean `not` and special forms `and` and `or`
1. `(define ... )` for "procedures" (functions)
1. Everything else in Scheme
