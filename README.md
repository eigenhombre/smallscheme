smallscheme
===========

<img src="/smallscheme.jpg" width="300">

![build](https://github.com/eigenhombre/smallscheme/actions/workflows/test.yml/badge.svg)

A small Scheme written in Python.

Originally written as a warmup exercise to prepare for [this
class](https://www.dabeaz.com/sicp.html).

`smallscheme` is not a complete R7RS Scheme (or R5RS for that matter) -- it implements
everything needed to follow along in
[SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs)
up to page **68**.  `smallscheme` is very lightweight and can be
installed on any Python 3 installation as follows:

# Install

    pip install smallscheme

# Usage

See [tests.scm](https://github.com/eigenhombre/smallscheme/blob/master/tests.scm) for many examples of the language in action.

## REPL

    $ smallscheme
    scheme> (define (fact n) (if (< n 2) n (* n (fact (- n 1)))))
    scheme> (fact 50)
    30414093201713378043612608166064768844377641568960512000000000000
    scheme> ^D
    $

The REPL comes with arrow-key history, line editing, and other features provided by [the Python Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/en/stable/).

## Running Programs

Example:

    $  cat fact.scm
    (define (fact n)
      (if (< n 2)
          n
          (* n (fact (- n 1)))))

    (define f100 (fact 100))

    (display f100)
    (newline)
    $  smallscheme fact.scm
    933262154439441526816992388562667004907159682643816214685929638
    952175999932299156089414639761565182862536979208272237582511852
    10916864000000000000000000000000
    $

# Language

`smallscheme` implements the basics of Scheme required to follow
examples or work problems in SICP, including the following:

## Primitive Functions

    *
    +
    -
    /
    <
    =
    >
    atan
    car
    cdr
    cons
    cos
    display
    newline
    not
    random
    remainder
    runtime
    sin

There are also two simple functions used in the Scheme-language tests: `is` and `test`; `test` currently behaves like a `progn` or `do` in other lisps, in that it collects multiple forms to be evaluated and returns the result of the last evaluation.  `is` is basically `assert`.
## Special Forms

    and
    cond
    define
    if
    lambda
    let
    or
    quote

For explanation of these, and of Scheme in general, I recommend
reading [Structure and Intepretation of Computer
Programs](https://mitpress.mit.edu/sites/default/files/sicp/index.html),
in print or (free!) online.

## Caveat

Not a production-ready language implementation -- error messages
and performance in particular may not be the best.

# Local Development

## Setup

    pip install -r requirements.txt

## Tests

Python tests are run with `pytest`.

Scheme tests are run with `./smallscheme/main.py -t tests.scm`.  These
tests are particularly helpful in seeing what's been implemented so
far.

# License

[MIT](https://github.com/eigenhombre/smallscheme/blob/master/LICENSE.txt)

Some code fragments used in tests are copied directly from SICP, which
is licensed with the Creative Commons "Attribution-ShareAlike 4.0
International (CC BY-SA 4.0)" license.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
