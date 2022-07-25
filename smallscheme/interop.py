from smallscheme.builtin import dispatch_table

def register_fn(fn_name, python_fn):
    dispatch_table[fn_name] = python_fn
