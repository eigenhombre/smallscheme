from smallscheme.builtin import dispatch_table

def register_fn(fn_name, python_fn):
    dispatch_table[fn_name] = python_fn

def scheme_fn(func):
    """
    Decorator which hides the detail of registering
    the function (which is not even wrapped!).

    >>> @scheme_fn
    >>> def inc(args):
    >>>     return int_(value(args[0]) + 1)
    """
    register_fn(func.__name__, func)
    return func
