smallscheme
===========

[![builds.sr.ht status](https://builds.sr.ht/~eigenhombre/smallscheme.svg)](https://builds.sr.ht/~eigenhombre/smallscheme?)

A tiny (< 400 lines) Scheme written in Python to prepare for [this
class](https://www.dabeaz.com/sicp.html).

Currently, this Scheme implements everything needed to follow along in
[SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs)
up to page **54**.

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

Making Programs
---------------
Example:

    $  cat test.scm
    (display (quote hello))
    (display (quote world))
    $  ./smallscheme/scheme.py test.scm
    hello
    world
    $

Done
----
1. Lexing and parsing of atoms and s-expressions
1. Read-Eval-Print
1. Special forms `quote if cond define or and lambda`
1. Functions `+ - / * = < > not car cdr cons remainder random`
1. Local (block or function level defines)
1. Program file evaluation (e.g., `scheme.py myprog.scm`)

Next steps
-----
1. `runtime` and `newline` functions
1. Python interop?
