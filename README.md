smallscheme
===========

[![builds.sr.ht status](https://builds.sr.ht/~eigenhombre/smallscheme.svg)](https://builds.sr.ht/~eigenhombre/smallscheme?)

A tiny scheme written in Python to prepare for
[this class](https://www.dabeaz.com/sicp.html).

Currently, this Scheme implements everything needed to follow along in [SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs) up through page **39**.

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
    scheme> (define (fact n) (if (< n 2) n (* n (fact (- n 1)))))
    scheme> (fact 50)
    30414093201713378043612608166064768844377641568960512000000000000
    scheme> ^D
    $

See `smallscheme/test_scheme.py` for many more examples.

Done
----
1. Lexing and parsing of atoms and s-expressions
1. Read-Eval-Print
1. Special forms
   1. `quote`
   1. `if` / `cond`
   1. `define`
   1. `or` / `and`
1. Functions `+ - / * = < > not car cdr cons`
1. Local (block or function level defines)

Next steps
-----
1. `lambda` application and higher order functions
1. Add program file evaluation (e.g., `scheme.py myprog.scm`)
1. PEP-8 auto lint
