smallscheme
===========

<img src="/smallscheme.jpg" width="300">

![build](https://github.com/eigenhombre/smallscheme/actions/workflows/test.yml/badge.svg)

A small Scheme written in Python.

Originally written as a warmup exercise to prepare for [this
class](https://www.dabeaz.com/sicp.html).

`smallscheme` is not a complete R7RS Scheme (or R5RS for that matter)
-- it implements everything needed to follow along in
[SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs)
up to page **102** (however, see "Limitations," below).  `smallscheme`
is very lightweight and can be installed on any Python 3 installation
as follows:

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

# Extending `smallscheme`

`smallscheme` is easily extendable using Python functions.

To add a new function to `smallscheme`, create a function which
accepts a list of arguments `args`.  These will have to be converted
into Python objects via the helper functions in `smallscheme.dtypes`.
For example, to create a function `inc` which increments its argument,

    from smallscheme.dtypes import *
    from smallscheme.interop import scheme_fn

    @scheme_fn
    def inc(args):
        assert len(args) == 1, "inc only takes one argument"
        arg_number = args[0]
        assert typeof(arg_number) in ['int', 'float'], "inc expects a number"
        num_value = value(arg_number)
        return int_(num_value + 1)

The `scheme_fn` decorator handles registration of your Python function
with the interpreter, which could also be registered explicitly, as follows:

    from smallscheme.interop import register_fn
    register_fn('inc', inc)

For function names which are valid in Scheme but not in Python (such
as `+`), you'll need to use `register_fn` rather than `scheme_fn`.

At the current time, any builtin function (but not special forms) can
be overridden using this mechanism.  There's [an example of
this](https://github.com/eigenhombre/smallscheme/blob/master/smallscheme/test_interop.py#L22)
in the tests.

Once your Python functions have been registered, your code can then
execute Scheme expressions, either by executing one or more Scheme
source files, or by launching a REPL for the user:

    import smallscheme

    smallscheme.run_file("myprogram.scm")

    # ... or ...:

    smallscheme.repl()

... and the new function can then be called from Scheme:

    scheme> (inc 1)
    ;;=>
    2

For a full list of data type operators (for converting from Python to
Scheme and vice-versa), look at
[dtypes.py](https://github.com/eigenhombre/smallscheme/blob/master/smallscheme/dtypes.py).
See also the sample program in the [examples
folder](https://github.com/eigenhombre/smallscheme/tree/master/examples).

# Caveats

Not a production-ready language implementation -- error messages and
performance in particular may not be the best.  Features used in later
parts of SICP may not be available yet. I have been implementing
them roughly in the order they are introduced.

The status of this work should be considered very alpha.  APIs and
implementation details may change.

# Limitations

`smallscheme` uses Python lists to represent Scheme lists.  As such it
does not support dotted-pair notation or `cons`ing onto a non-list.
This will require slight changes in a few of the examples in SICP.
The pair representation of rational numbers in Chapter 2, for example,
would need to be adapted to use lists of two numbers rather than a
single cons pair.

# Local Development

## Setup

    pip install -r requirements.txt

## Tests

Python tests are run with `pytest`.

Scheme tests are run with `./smallscheme/main.py -t tests.scm`.  These
tests are particularly helpful in seeing what's been implemented so
far.

# See Also

- [Original blog post](http://johnj.com/posts/scheme-in-python/) introducing `smallscheme`
- Structure and Interpretation of Computer Programs [Web site](https://mitpress.mit.edu/sites/default/files/sicp/index.html)
- P. Norvig, [(How to Write a (Lisp) Interpreter (in Python))](http://www.norvig.com/lispy.html)
- `l1`, [a simple Lisp written in Go](http://johnj.com/posts/l1/) by the author

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
