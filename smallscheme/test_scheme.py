import sys
from smallscheme.dtypes import *
from smallscheme.parse import parse_str
from smallscheme.scheme import evalu, printable_value
from smallscheme.test_util import teq

def test_evalu():
    """
    Thin, lower-level smoke test of `evalu` function.  Much more
    testing of evaluation is done in tests.scm.
    """
    def t(a, b):
        teq(evalu(a, {}), b)
    t(int_(1234), int_(1234))
    t(int_(1234), int_(1234))
    t(TRUE, TRUE)
    t(FALSE, FALSE)
    t(atom('+'), ('intproc', '+'))
    t(list_([atom('quote'),
             int_(3)]),
      int_(3))
    t(list_([atom('quote'),
             list_([atom('a'),
                    atom('b'),
                    atom('c')])]),
      list_([atom('a'),
             atom('b'),
             atom('c')]))

def single_eval_check(s1, s2, env):
    teq(printable_value(evalu(parse_str(s1)[0],
                              env)),
        s2)

def multiple_eval_check(s1, env, *s2):
    ret = None
    for p in parse_str(s1):
        ret = evalu(p, env)
    if s2:
        teq(printable_value(ret), s2[0])

def test_printable_value():
    def t(s1, *s2):
        multiple_eval_check(s1, {}, *s2)

    t("+", "Internal procedure '+'")
    t("/", "Internal procedure '/'")
    t("(quote a)", "a")
    t("()", "()")
    t("(quote 0)", "0")
    t("(quote (1 2 3))", "(1 2 3)")
    t("(quote (a b c))", "(a b c)")
    t("""(+ 1
            2
            3)""", "6")
    t("""(+ (* 3
               (+ (* 2 4)
                  (+ 3 5)))
            (+ (- 10 7)
               6))""", "57")

def test_define():
    def t(a, b, env1):
        env = {}
        teq(printable_value(evalu(parse_str(a)[0],
                                  env)), b)
        assert env == env1, (
            "Environment mismatch: '%s' vs '%s'" %
            (env, env1))

    t("(define size 2)", "", {'size': int_(2)})

def test_runtime():
    env = {}
    assert type(evalu(parse_str("(runtime)")[0],
                      env)) is int

def test_random():
    for _ in range(50):
        t, v = evalu(parse_str("(random 10)")[0], {})
        assert t == 'int'
        assert 0 <= v < 10
