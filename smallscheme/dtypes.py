def atom(x):
    return 'atom', x

def list_(x):
    return 'list', x

def bool_(x):
    return 'bool', x

def int_(x):
    return 'int', x

def float_(x):
    return 'float', x

def make_fn(fn_name, args, body, env):
    return 'fn', (fn_name, args, body, env)

def typeof(x):
    return x[0]

def value(x):
    return x[1]

noop = 'nop', None

def printable_value(ast):
    typ, val = typeof(ast), value(ast)
    if typ == 'int' or typ == 'float':
        return str(val)
    if typ == 'bool':
        return {True: "#t",
                False: "#f"}.get(val)
    if typ == 'intproc':
        return "Internal procedure '%s'" % val
    if typ == 'atom':
        return val
    if typ == 'list':
        return '(' + ' '.join([printable_value(x)
                               for x in val]) + ')'
    if typ == 'nop':
        return ''
    if typ == 'fn':
        (fn_name, _, _) = val
        if fn_name == 'lambda':
            return "Anonymous-function"
        return "Function-'%s'" % str(fn_name)

    raise Exception('Unprintable ast "%s"' % str(ast))

AND       = atom('and')
COND      = atom('cond')
DEFINE    = atom('define')
IF        = atom('if')
LAMBDA    = atom('lambda')
LET       = atom('let')
OR        = atom('or')
QUOTE     = atom('quote')
TRUE      = bool_(True)
FALSE     = bool_(False)
EMPTYLIST = list_([])
