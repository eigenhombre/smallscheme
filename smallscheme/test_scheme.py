from smallscheme.scheme import *
from pprint import pformat

def teq(a, b):
    assert a == b, "\n%s\n!=\n%s" % (pformat(a), pformat(b))

def test_parse_str():
    def t(a, b):
        teq(parse_str(a), b)
    t("1234", ('int', 1234))
    t("3.1415", ('float', 3.1415))
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
    # Adapted from SICP p. 8:
    evalu(parse_str("(define pi 3.14159)"), env)
    evalu(parse_str("(define radius 10)"), env)
    teq(printable_value(evalu(parse_str(
        "(* pi (* radius radius))"), env)),
        "314.159")
    evalu(parse_str("(define circumference (* 2 pi radius))"),
          env)
    teq(printable_value(evalu(parse_str(
        "circumference"), env)), "62.8318")
