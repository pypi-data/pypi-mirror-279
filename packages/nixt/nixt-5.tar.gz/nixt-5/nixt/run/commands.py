# This file is placed in the Public Domain.
#
#


"commands"


import inspect


from nixt.lib.object import Object
from nixt.run.parse  import parse
from nixt.run.utils  import spl


class Commands:

    "Commands"

    cmds = Object()

    @staticmethod
    def add(func):
        "add command."
        setattr(Commands.cmds, func.__name__, func)

    @staticmethod
    def scan(mod) -> None:
        "scan module for commands."
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz)


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Commands.cmds, evt.cmd, None)
    if func:
        func(evt)
    bot.show(evt)
    evt.ready()


def scan(pkg, modstr):
    "scan modules for commands and classes"
    mds = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        Commands.scan(module)
    return mds


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
