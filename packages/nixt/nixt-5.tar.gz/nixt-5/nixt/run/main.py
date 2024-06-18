# This file is placed in the Public Domain.
#
# pylint: disable=C0103,C0413,C0415,E0401


"runtime"


import getpass
import os
import sys
import time


from nixt.run.commands import command, scan
from nixt.lib.config   import Config
from nixt.run.broker   import Broker
from nixt.run.cli      import CLI
from nixt.run.console  import Console
from nixt.run.errors   import errors
from nixt.run.event    import Event
from nixt.run.help     import __doc__ as helpstring
from nixt.run.parse    import parse
from nixt.run.persist  import Persist, skel
from nixt.run.utils    import daemon, getmods, privileges, wrap


Cfg         = Config()
Cfg.dis     = ""
Cfg.mod     = "cmd,err,mod,thr"
Cfg.opts    = ""
Cfg.name    = "nixt"
Cfg.version = "5"
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.moddir  = os.path.join(Cfg.wdr, "mods")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


broker = Broker()


import nixt.mod as modules


def cmnd(txt, outer):
    "do a command using the provided output function."
    cli = CLI()
    cli.out = outer
    evn = Event()
    evn.txt = txt
    command(cli, evn)
    evn.wait()
    return evn


def wrapped():
    "wrap main."
    wrap(main)
    errors()


def main():
    "main"
    skel()
    parse(Cfg, " ".join(sys.argv[1:]))
    mods = getmods(Cfg)
    if "a" in Cfg.opts:
        Cfg.mod = ",".join(dir(modules))
        if mods:
            Cfg.mod += "," + ",".join(dir(mods))
    if "h" in Cfg.opts:
        print(helpstring)
        return
    if "v" in Cfg.opts:
        dte = " ".join(time.ctime(time.time()).replace("  ", " ").split()[1:])
        print(f'{dte} {Cfg.name.upper()} {Cfg.opts.upper()} {Cfg.mod.upper()}'.replace("  ", " "))
    if "d" in Cfg.opts:
        Cfg.mod  = ",".join(dir(modules))
        Cfg.user = getpass.getuser()
        daemon(Cfg.pidfile, "-v" in sys.argv)
        privileges(Cfg.user)
        scan(modules, Cfg.mod)
        scan(mods, Cfg.mod)
        cmnd(Cfg.otxt, print)
        while 1:
            time.sleep(1.0)
        return
    scan(modules, Cfg.mod)
    scan(mods, Cfg.mod)
    if "c" in Cfg.opts:
        cmnd(Cfg.otxt, print)
        csl = Console()
        csl.out = print
        csl.start()
        while 1:
            time.sleep(1.0)
    elif Cfg.otxt:
        cmnd(Cfg.otxt, print)
    if "w" in Cfg.opts:
        while 1:
            time.sleep(1.0)


def __dir__():
    return (
        'Cfg',
        'broker',
        'cmnd',
        'main',
        'wrapped'
    )
