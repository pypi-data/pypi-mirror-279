# This file is placed in the Public Domain.
#
# pylint: disable=C0413,W0105


"objects"


import os
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from nixt.lib.default import Default
from nixt.run.handler import CLI, Commands, Event, Handler, cmnd, command, scan
from nixt.run.persist import Persist
from nixt.run.utils   import parse


from nixt import mod as MODS


Cfg         = Default()
Cfg.debug   = True
Cfg.mod     = ""
Cfg.name    = "nixt"
Cfg.silent  = False
Cfg.version = "83"
Cfg.wdr     = ".test"


class Console(CLI):

    "Console"

    def announce(self, txt):
        "disable announce."

    def callback(self, evt):
        "wait for callback."
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(list(Commands.cmds))))


def wrap(func):
    "reset terminal."
    old3 = None
    try:
        old3 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old3:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old3)


def main():
    "main"
    Persist.workdir = Cfg.wdr
    Commands.add(cmd)
    Cfg.mod = ",".join(dir(MODS))
    parse(Cfg, " ".join(sys.argv[1:]))
    if "v" in Cfg.opts:
        dte = " ".join(time.ctime(time.time()).replace("  ", " ").split()[1:])
        print(f'{dte} {Cfg.name.upper()} {Cfg.opts.upper()} {Cfg.mod.upper()}'.replace("  ", " "))
    scan(MODS, Cfg.mod)
    if "c" in Cfg.opts:
        csl = Console()
        csl.out = print
        csl.start()
        while 1:
            time.sleep(1.0)
    elif Cfg.otxt:
        cmnd(Cfg.otxt, print)


if __name__ == "__main__":
    wrap(main)
