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

def typeof(x):
    return x[0]

def value(x):
    return x[1]

noop = 'nop', None

def printable_value(ast):
    k, v = ast
    if k == 'int' or k == 'float':
        return str(v)
    if k == 'bool':
        return {True: "#t",
                False: "#f"}.get(v)
    if k == 'intproc':
        return "Internal procedure '%s'" % v
    if k == 'atom':
        return v
    if k == 'list':
        return '(' + ' '.join([printable_value(x)
                               for x in v]) + ')'
    if k == 'nop':
        return ''
    if k == 'fn':
        (fn_name, _, _) = v
        if fn_name == 'lambda':
            return "Anonymous-function"
        return "Function-'%s'" % str(fn_name)
    raise Exception('Unprintable ast "%s"' % str(ast))

QUOTE  = atom('quote')
COND   = atom('cond')
IF     = atom('if')
DEFINE = atom('define')
LAMBDA = atom('lambda')
OR     = atom('or')
AND    = atom('and')
TRUE   = bool_(True)
FALSE  = bool_(False)
