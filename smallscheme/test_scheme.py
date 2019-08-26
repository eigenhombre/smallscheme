from smallscheme.scheme import *
from pprint import pformat

def teq(a, b):
    assert a == b, "\n%s\n!=\n%s" % (pformat(a), pformat(b))

def test_parse_str():
    def t(a, b):
        teq(parse_str(a), b)
    t("1234", ('int', 1234))
    t("-1234", ('int', -1234))
    t("+1234", ('int', 1234))
    t("3.1415", ('float', 3.1415))
    t("+3.1415", ('float', 3.1415))
    t("-3.1415", ('float', -3.1415))
    t("x", ('atom', 'x'))
    t("y", ('atom', 'y'))
    t("yxyz", ('atom', 'yxyz'))
    t("#t", ("bool", True))
    t("#f", ("bool", False))
    t("(a)", ('list', [('atom', 'a')]))
    t("(a 1 2)", ('list', [('atom', 'a'),
                           ('int', 1),
                           ('int', 2)]))
    t("(+ 2 3)", ('list', [('atom', '+'),
                           ('int', 2),
                           ('int', 3)]))
    t("(a 1 (b foo x3))",
      ('list', [('atom', 'a'),
                ('int', 1),
                ('list', [('atom', 'b'),
                          ('atom', 'foo'),
                          ('atom', 'x3')])]))
    t("(())", ("list", [("list", [])]))
    t("((a))", ("list", [("list", [('atom', 'a')])]))
    t("((a b))", ("list", [("list", [('atom', 'a'),
                                     ('atom', 'b')])]))
    t("(a (b))", ("list", [("atom", "a"),
                           ("list", [("atom", "b")])]))
    t("((a) b)", ("list", [("list", [("atom", "a")]),
                           ("atom", "b")]))
    t("(a (b c) d)", ('list', [('atom', 'a'),
                               ('list', [('atom', 'b'),
                                         ('atom', 'c')]),
                               ('atom', 'd')]))
    t("(+ (* 2 4) (+ 3 5))",
      ('list', [('atom', '+'),
                ('list', [('atom', '*'),
                          ('int', 2),
                          ('int', 4)]),
                ('list', [('atom', '+'),
                          ('int', 3),
                          ('int', 5)])]))

def test_evalu():
    def t(a, b):
        teq(evalu(a, {}), b)
    t(('int', 1234), ('int', 1234))
    t(('int', 1234), ('int', 1234))
    t(('bool', True), ('bool', True))
    t(('bool', False), ('bool', False))
    t(('atom', '+'), ('intproc', '+'))
    t(('list', [('atom', 'quote'),
                ('int', 3)]),
      ('int', 3))
    t(('list', [('atom', 'quote'),
                ('list', [('atom', 'a'),
                          ('atom', 'b'),
                          ('atom', 'c')])]),
      ('list', [('atom', 'a'),
                          ('atom', 'b'),
                          ('atom', 'c')]))

def test_printable_value():
    def t(a, b):
        teq(printable_value(evalu(parse_str(a),
                                  {})), b)

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
        teq(printable_value(evalu(parse_str(a),
                                  env)), b)
        assert env == env1, (
            "Environment mismatch: '%s' vs '%s'" %
            (env, env1))

    t("(define size 2)", "", {'size': ('int', 2)})

def test_multiple_defines():
    env = {}
    def e(s):
        evalu(parse_str(s), env)
    def t(s1, s2):
        teq(printable_value(evalu(parse_str(
            s1), env)), s2)
    # Adapted from SICP p. 8:
    e("(define pi 3.14159)")
    e("(define radius 10)")
    t("(* pi (* radius radius))", "314.159")
    e("(define circumference (* 2 pi radius))")
    t("circumference", "62.8318")
    # p. 19:
    e("(define x 7)")
    t("(and (> x 5) (< x 10))", "#t")
    t("(car (quote (1 2 3)))", "1")
    t("(car (quote (a b c)))", "a")
    t("(cdr (quote (1 2 3)))", "(2 3)")
    t("(cdr (quote (a b c)))", "(b c)")

def test_define_function():
    env = {}
    def e(s):
        evalu(parse_str(s), env)
    def t(s1, s2):
        teq(printable_value(evalu(parse_str(
            s1), env)), s2)

    e("(define (square x) (* x x))")
    t("square", "Function 'square'")
    e("(define (f x y) (+ x y))")
    e("(define z 33)")
    t("(square 21)", "441")
    t("(square (+ 2 5))", "49")
    t("(square (square 3))", "81")
    e("""(define (sum-of-squares x y)
           (+ (square x) (square y)))""")
    t("(sum-of-squares 3 4)", "25")
    e("""(define (f a)
           (sum-of-squares (+ a 1) (* a 2)))""")
    t("(f 5)", "136")

    e("""(define (abs x)
           (cond ((> x 0) x)
                 ((= x 0) 0)
                 ((< x 0) (- x))))""")
    t("(abs 10)", "10")
    t("(abs -10)", "10")

    e("""(define (abs x)
           (cond ((< x 0) (- x))
                 (else x)))""")
    t("(abs 10)", "10")
    t("(abs -10)", "10")

    e("""(define (abs x)
           (if (< x 0)
               (- x)
               x))""")
    t("(abs 10)", "10")
    t("(abs -10)", "10")

    e("""(define (fact n)
           (if (< n 2)
               n
               (* n (fact (- n 1)))))""")
    t("(fact 1)", "1")
    t("(fact 2)", "2")
    t("(fact 3)", "6")
    t("(fact 10)", "3628800")

    # P. 23-24:
    e("""(define (sqrt-iter guess x)
           (if (good-enough? guess x)
               guess
               (sqrt-iter (improve guess x)
                          x)))""")
    e("""(define (improve guess x)
           (average guess (/ x guess)))""")
    e("""(define (average x y)
           (/ (+ x y) 2))""")
    e("""(define (good-enough? guess x)
           (< (abs (- (square guess) x)) 0.001))""")
    e("""(define (sqrt x)
           (sqrt-iter 1.0 x))""")
    # These may or may not pass; they do on my
    # Macbook Pro:
    # t("(sqrt 9)", "3.0")
    # t("(square (sqrt 100))", "100.0")
    e("""(define (a) 3)""")
    t("(a)", "3")
    e("""(define (a) (+ 1 2))""")
    t("(a)", "3")
    e("""(define (a) 1 666)""")
    t("(a)", "666")
    e("""(define (a)
           (define b 3)
           b)""")
    t("(a)", "3")
    e("""(define (a)
           (define (f) 4)
           (f))""")
    t("(a)", "4")

    t("+", "Internal procedure '+'")
    e("(define round square)")
    t("(round 5)", "25")

    # TODO:
    # t("((lambda (x) 3) 1)", "3")
