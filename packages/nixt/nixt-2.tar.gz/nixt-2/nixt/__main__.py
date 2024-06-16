# This file is placed in the Public Domain.
#
# pylint: disable=C0413,W0105


"""NIXT - you have been nixt.

    nixt  <cmd> [key=val] [key==val]
    nixt  [-a] [-c] [-h] [-v]

    options are:

    -a     load all modules
    -c     start console
    -h     show help
    -v     use verbose

    the cmd command show available commands.
    
    $ nixt cmd
    cfg,cmd,dpl,err,exp,imp,mod,mre,nme,pwd,rem,res,rss,thr

"""


import os
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from nixt.lib.default import Default
from nixt.run.handler import CLI, Commands, Event, Handler, cmnd, command, scan
from nixt.run.persist import Persist
from nixt.run.utils   import parse


from nixt import mod as modules


Cfg             = Default()
Cfg.dis         = ""
Cfg.mod         = "cmd,err,fnd,log,mod,tdo,thr,tmr"
Cfg.opts        = ""
Cfg.name        = "nixt"
Cfg.version     = "2"
Cfg.wdr         = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile     = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")



if os.path.exists("mods"):
     import mods
else:
     mods = None


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


def daemon(pidfile, verbose=False):
    "switch to background."
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    path = pathlib.Path(pidfile)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges(username):
    "drop privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


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
    Cfg.mod = ",".join(dir(modules))
    Persist.workdir = Cfg.wdr
    Persist.skel()
    parse(Cfg, " ".join(sys.argv[1:]))
    if mods:
        Cfg.mod += "," + ",".join(dir(mods))
    if "v" in Cfg.opts:
        dte = " ".join(time.ctime(time.time()).replace("  ", " ").split()[1:])
        print(f'{dte} {Cfg.name.upper()} {Cfg.opts.upper()} {Cfg.mod.upper()}'.replace("  ", " "))
    if "d" in Cfg.opts:
        Cfg.mod  = ",".join(dir(modules))
        Cfg.user = getpass.getuser()
        daemon(Cfg.pidfile, "-v" in sys.argv)
        privileges(Cfg.user)
        scan(modules, Cfg.mod)
        while 1:
            time.sleep(1.0)
        return
    scan(modules, Cfg.mod)
    scan(mods, Cfg.mod)
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
