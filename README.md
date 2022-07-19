smallscheme
===========

<img src="/smallscheme.jpg" width="300">

![build](https://github.com/eigenhombre/smallscheme/actions/workflows/test.yml/badge.svg)

A tiny (< 400 lines) Scheme written in Python to prepare for [this
class](https://www.dabeaz.com/sicp.html).

Currently, this Scheme implements everything needed to follow along in
[SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs)
up to page **54**.

# Install

    pip install smallscheme

# Usage

## REPL

Use `rlwrap` if you want history and that sort of thing:

    $ rlwrap smallscheme
    scheme> (define (fact n) (if (< n 2) n (* n (fact (- n 1)))))
    scheme> (fact 50)
    30414093201713378043612608166064768844377641568960512000000000000
    scheme> ^D
    $

See [test_scheme.py](https://github.com/eigenhombre/smallscheme/blob/master/smallscheme/test_scheme.py) for many more examples.

## Running Programs

Example:

    $  cat test.scm
    (define (fact n)
      (if (< n 2)
          n
          (* n (fact (- n 1)))))

    (define f10 (fact 10))

    (display f10)
    $  ./smallscheme/scheme.py test.scm
    3628800
    $

# Language

Implemented so far:

## Functions

    *
    +
    -
    /
    <
    =
    >
    car
    cdr
    cons
    display
    not
    random
    remainder

## Special Forms

    and
    cond
    define
    if
    lambda
    or
    quote

# Local Development

## Setup

    pip install -r requirements.txt

## Tests

    pytest

# Done

1. Lexing and parsing of atoms and s-expressions
1. Read-Eval-Print
1. Special forms `quote if cond define or and lambda`
1. Functions `+ - / * = < > not car cdr cons remainder random`
1. Local (block or function level defines)
1. Program file evaluation (e.g., `scheme.py myprog.scm`)

# Next steps

1. Go further in SICP for examples / tests / requirements
1. `runtime` and `newline` functions
1. Python interop?

# License

[MIT](https://github.com/eigenhombre/smallscheme/blob/master/LICENSE.txt)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
