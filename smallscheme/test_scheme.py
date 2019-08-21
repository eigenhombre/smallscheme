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
