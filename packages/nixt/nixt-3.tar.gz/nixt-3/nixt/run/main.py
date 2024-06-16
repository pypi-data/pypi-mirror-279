# This file is placed in the Public Domain.


"runtime"


import os


from nixt.lib.config import Config
from nixt.run.broker import Broker


Cfg         = Config()
Cfg.dis     = ""
Cfg.mod     = "cmd,err,fnd,log,mod,tdo,thr,tmr"
Cfg.opts    = ""
Cfg.name    = "nixt"
Cfg.version = "3"
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


broker = Broker()


def __dir__():
    return (
        'Cfg',
        'broker'
    )
