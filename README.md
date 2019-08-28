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
