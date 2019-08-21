from smallscheme.scheme import *

def test_parse_str():
    assert (parse_str("x") == {'atom': 'x'})
    assert (parse_str("y") == {'atom': 'y'})
    assert (parse_str("yxyz") == {'atom': 'yxyz'})
    assert (parse_str("1234") == {'num': 1234})
    assert (parse_str("(a)") == {'list': [{'atom': 'a'}]})
    assert (parse_str("(a 1 1)")
            ==
            {'list': [{'atom': 'a'}, {'num': 1}, {'num': 1}]})
    assert (parse_str("(+ 2 3)")
            ==
            {'list': [{'atom': '+'}, {'num': 2}, {'num': 3}]})
    assert (parse_str("(a 1 (b foo x3))")
            ==
            {'list': [{'atom': 'a'},
                      {'num': 1},
                      {'list': [{'atom': 'b'},
                                {'atom': 'foo'},
                                {'atom': 'x3'}]}]})
    assert (parse_str("#t") == {'bool': True})
    assert (parse_str("#f") == {'bool': False})

def test_evalu():
    assert evalu({'num': 1234}) == {'num': 1234}
    assert evalu({'bool': True}) == {'bool': True}
    assert evalu({'bool': False}) == {'bool': False}
    assert evalu({'atom': '+'}) == {'intproc': '+'}
    assert (evalu({'list': [{'atom': 'quote'},
                            {'num': 3}]})
            ==
            {'num': 3})
    assert (evalu({'list': [{'atom': 'quote'},
                            {'list': [{"atom": "a"},
                                      {"atom": "b"},
                                      {"atom": "c"}]}]})
            ==
            {'list': [{"atom": "a"},
                                      {"atom": "b"},
                                      {"atom": "c"}]})

def test_printable_value():
    def t(a, b):
        a = printable_value(evalu(parse_str(a)))
        assert a == b, "'%s' != '%s'" % (a, b)
    t("1234", "1234")
    t("+", "Internal procedure '+'")
    t("#f", "#f")
    t("#t", "#t")
    t("()", "()")
    t("(quote a)", "a")
    t("(quote 0)", "0")
    t("(quote (1 2 3))", "(1 2 3)")
    t("(quote (a b c))", "(a b c)")
