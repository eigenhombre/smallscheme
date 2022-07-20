from scheme import *

def intern_scheme_fn_data(env, fname, argsyms, *body):
    intern_fn(env, fname, argsyms, body)

def test_hooks():
    base_env = {}
    intern_scheme_fn_data(
        base_env,
        'is',
        [atom('arg')],
        int_(3),
        int_(4)
    )
    intern_fn(base_env,
              'test',
              [('atom', 'arg')],
              [('int', 4)])
    return base_env
