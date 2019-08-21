from smallscheme.scheme import *
from pprint import pformat

def teq(a, b):
    assert a == b, "%s\n!=\n%s" % (pformat(a), pformat(b))

def test_parse_str():
    def t(a, b):
        teq(parse_str(a), b)
    t("x", ('atom', 'x'))
    t("y", ('atom', 'y'))
    t("yxyz", ('atom', 'yxyz'))
    t("1234", ('num', 1234))
    t("#t", ("bool", True))
    t("#f", ("bool", False))
    t("(a)", ('list', [('atom', 'a')]))
    t("(a 1 2)", ('list', [('atom', 'a'),
                           ('num', 1),
                           ('num', 2)]))
    t("(+ 2 3)", ('list', [('atom', '+'),
                           ('num', 2),
                           ('num', 3)]))
    t("(a 1 (b foo x3))",
      ('list', [('atom', 'a'),
                ('num', 1),
                ('list', [('atom', 'b'),
                          ('atom', 'foo'),
                          ('atom', 'x3')])]))
    t("(a (b c) d)", ('list', [('atom', 'a'),
                               ('list', [('atom', 'b'),
                                         ('atom', 'c')]),
                               ('atom', 'd')]))
    # FIXME:
    # t("(+ (* 2 4) (+ 3 5))",
    #   ('list', [('atom', '+'),
    #             ('list', [('atom', '*'),
    #                       ('num', 2),
    #                       ('num', 4)]),
    #             ('list', [('atom', '+'),
    #                       ('num', 3),
    #                       ('num', 5)])]))

def test_evalu():
    def t(a, b):
        teq(evalu(a), b)
    t(('num', 1234), ('num', 1234))
    t(('num', 1234), ('num', 1234))
    t(('bool', True), ('bool', True))
    t(('bool', False), ('bool', False))
    t(('atom', '+'), ('intproc', '+'))
    t(('list', [('atom', 'quote'),
                ('num', 3)]),
      ('num', 3))
    t(('list', [('atom', 'quote'),
                ('list', [('atom', 'a'),
                          ('atom', 'b'),
                          ('atom', 'c')])]),
      ('list', [('atom', 'a'),
                          ('atom', 'b'),
                          ('atom', 'c')]))

def test_printable_value():
    def t(a, b):
        teq(printable_value(evalu(parse_str(a))), b)

    t("1234", "1234")
    t("#f", "#f")
    t("#t", "#t")
    t("+", "Internal procedure '+'")
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
    t("(+ 3 5)", "8")
    t("(* 2 4)", "8")
    # FIXME:
    #t("(+ (* 2 4) (+ 3 5))", "16")
    # t("""(+ (* 3
    #            (+ (* 2 4)
    #               (+ 3 5)))
    #         (+ (- 10 7)
    #            6))""", "3")
