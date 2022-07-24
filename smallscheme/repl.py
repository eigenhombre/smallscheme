# prompt_toolkit setup example taken from
# https://stackoverflow.com/questions/59627995:
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from os.path import expanduser

from smallscheme.env import Env
from smallscheme.scheme import parse_str, evalu, printable_value


def repl():
    session = PromptSession(history=FileHistory(
        expanduser('~/.smallscheme_history')))

    env = Env()
    while True:
        try:
            x = session.prompt("scheme> ").strip()
        except EOFError:
            print()
            break
        if x:
            try:
                for parsed in parse_str(x):
                    pv = printable_value(evalu(parsed, env))
                    if pv:
                        print(pv)
            except Exception as e:
                print(e)
