import sys
from smallscheme.scheme import *
from smallscheme.test_util import teq

def test_evalu():
    """
    Thin, lower-level smoke test of `evalu` function.  Much more
    testing of evaluation is done below.
    """
    def t(a, b):
        teq(evalu(a, {}), b)
    t(int_(1234), int_(1234))
    t(int_(1234), int_(1234))
    t(bool_(True), bool_(True))
    t(bool_(False), bool_(False))
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

    t("1234", "1234")
    t("#f", "#f")
    t("#t", "#t")
    t("+", "Internal procedure '+'")
    t("/", "Internal procedure '/'")
    t("(quote a)", "a")
    t("()", "()")
    t("(quote 0)", "0")
    t("(quote (1 2 3))", "(1 2 3)")
    t("(quote (a b c))", "(a b c)")
    t("(+ 1 1)", "2")
    t("(+ 1 2 3)", "6")
    t("(+ 1 2 (+ 1 1 1))", "6")
    t("(* 1 1)", "1")
    t("(* 1 2 3 4 5)", "120")
    t("""(+ 1
            2
            3)""", "6")
    t("(- 10 7)", "3")
    t("(- 10)", "-10")
    t("(/ 10 5)", "2")
    t("(/ 16 2 2 2)", "2")
    t("(+ 3 5)", "8")
    t("(* 2 4)", "8")
    t("(+ (* 2 4) (+ 3 5))", "16")
    t("""(+ (* 3
               (+ (* 2 4)
                  (+ 3 5)))
            (+ (- 10 7)
               6))""", "57")
    t("(= 1 1)", "#t")
    t("(= 1 2)", "#f")
    t("(= 1 (quote notone))", "#f")
    t("(= #t #t)", "#t")
    t("(not #t)", "#f")
    t("(not #f)", "#t")
    t("(not 1)", "#f")
    t("(> 2 1)", "#t")
    t("(> 1 2)", "#f")
    t("(< 2 1)", "#f")
    t("(< 1 2)", "#t")
    # FIXME: higher arities of < and >.
    t("(cond (#t #t))", "#t")
    t("(cond (#t 3))", "3")
    t("(cond (#t #f))", "#f")
    t("(cond (#f #f) (#t #f))", "#f")
    t("(cond (#f #f) (#t #t))", "#t")
    t("(cond (#f #f) (else #t))", "#t")
    t("(if #t 1 2)", "1")
    t("(if #f 1 2)", "2")
    t("(or)", "#f")
    t("(or 1)", "1")
    t("(or #f 1)", "1")
    t("(or 1 1)", "1")
    t("(and)", "#t")
    t("(and #t)", "#t")
    t("(and 1 #t)", "#t")
    t("(and #t 1)", "1")
    t("(and #t #f)", "#f")
    t("(and #f #f)", "#f")

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

def test_multiple_defines():
    env = {}
    def t(s1, *s2):
        multiple_eval_check(s1, env, *s2)
    # Adapted from SICP p. 8:
    t("(define pi 3.14159)")
    t("(define radius 10)")
    t("(* pi (* radius radius))", "314.159")
    t("(define circumference (* 2 pi radius))")
    t("circumference", "62.8318")
    # p. 19:
    t("(define x 7)")
    t("(and (> x 5) (< x 10))", "#t")
    t("(car (quote (1 2 3)))", "1")
    t("(car (quote (a b c)))", "a")
    t("(cdr (quote (1 2 3)))", "(2 3)")
    t("(cdr (quote (a b c)))", "(b c)")

def test_random():
    for _ in range(50):
        t, v = evalu(parse_str("(random 10)")[0], {})
        assert t == 'int'
        assert 0 <= v < 10
