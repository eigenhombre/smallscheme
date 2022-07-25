import subprocess
import smallscheme
from smallscheme.dtypes import value, noop, atom, list_

def sh(args):
    return subprocess.check_output(args)

def say(args):
    """
    Use the Mac's `say` command to speak out loud the contents of
    the first argument, which should be a list.

    scheme> (say (quote (hello world)))
    scheme>
    """
    arglist = value(args[0])
    say_args = [str(value(arg)) for arg in arglist]
    sh(["say"] + say_args)
    return noop

def lastusers(_):
    """
    Return a Scheme list containing atoms corresponding to the
    users of the system returned by the `last` command (tested
    on MacOS only).

    scheme> (lastusers)
    (john admin john reboot wtmp)
    """

    user_lines = sh(["last"]).decode("utf-8").splitlines()
    users = [str(s).split(" ")[0] for s in user_lines[:-1]]
    return list_([atom(u) for u in users if u != ''])

if __name__ == "__main__":
    smallscheme.register_fn('say', say)
    smallscheme.register_fn('lastusers', lastusers)
    smallscheme.run_file("interop_example.scm")
