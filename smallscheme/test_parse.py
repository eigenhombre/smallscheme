from smallscheme.scheme import *
from smallscheme.test_util import teq

def test_parse_str():
    def t(a, b):
        teq(parse_str(a)[0], b)
    t("1234", int_(1234))
    t("-1234", int_(-1234))
    t("+1234", int_(1234))
    t("3.1415", float_(3.1415))
    t("+3.1415", float_(3.1415))
    t("-3.1415", float_(-3.1415))
    t("1", int_(1))
    t("1;", int_(1))
    t("1 ;; hello, I'm a comment", int_(1))
    t("""1 ;; a comment and a newline
""", int_(1))
    t("x", atom('x'))
    t("y", atom('y'))
    t("yxyz", atom('yxyz'))
    t("#t", bool_(True))
    t("#f", bool_(False))
    t("(a)", list_([atom('a')]))
    t("(a 1 2)", list_([atom('a'),
                        int_(1),
                        int_(2)]))
    t("(+ 2 3)", list_([atom('+'),
                        int_(2),
                        int_(3)]))
    t("(a 1 (b foo x3))",
      list_([atom('a'),
             int_(1),
             list_([atom('b'),
                    atom('foo'),
                    atom('x3')])]))
    t("(())", list_([list_([])]))
    t("((a))", list_([list_([atom('a')])]))
    t("((a b))", list_([list_([atom('a'),
                               atom('b')])]))
    t("(a (b))", list_([("atom", "a"),
                        list_([("atom", "b")])]))
    t("((a) b)", list_([list_([("atom", "a")]),
                        ("atom", "b")]))
    t("(a (b c) d)", list_([atom('a'),
                            list_([atom('b'),
                                   atom('c')]),
                            atom('d')]))
    t("(+ (* 2 4) (+ 3 5))",
      list_([atom('+'),
             list_([atom('*'),
                    int_(2),
                    int_(4)]),
             list_([atom('+'),
                    int_(3),
                    int_(5)])]))
