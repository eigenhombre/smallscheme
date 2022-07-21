import lark
from smallscheme.dtypes import *

grammar = '''
start  : _exprs
_exprs : _e* _e
_e     : ATOM
       | _num
       | BOOL
       | list
TRUE   : "#t"
FALSE  : "#f"
BOOL   : TRUE | FALSE
list   : "(" _exprs? ")"
INT    : /[-+]?[0-9]+/
ATOM   : /[a-zA-Z]+[a-zA-Z0-9\-\?\!]*/
       | /[\*\/\=\>\<]/
       | /[\-\+](?![0-9])/
FLOAT  : /[-+]?[0-9]+\.[0-9]*/
_num   : INT | FLOAT
COMMENT : ";" /(.)*/ NEWLINE?

%import common.WS
%import common.NEWLINE
%ignore WS
%ignore COMMENT
    '''

parser = lark.Lark(grammar)

def convert_ast(ast):
    """
    Re-cast the Lark representation of the parse tree into our own.

    'start' is always the top of the tree and `convert_ast` returns a
    list of zero or more parsed expressions.

    All other entrypoints are recursively converted into the
    appropriate atom, list, int, float etc.
    """
    if type(ast) is lark.tree.Tree:
        if ast.data == "start":
            return [convert_ast(x) for x in ast.children]
        if ast.data == "list":
            return list_([convert_ast(x) for x in ast.children])
    if type(ast) is lark.lexer.Token:
        ty = ast.type.lower()
        if ty == "int":
            return int_(int(ast.value))
        if ty == "float":
            return float_(float(ast.value))
        elif ty == "bool":
            return bool_(True if ast.value == "#t" else False)
        elif ty == "atom":
            return atom(ast.value)
    raise Exception("Unparsed AST: '%s'" % ast)

def parse_str(x):
    return convert_ast(parser.parse(x))
