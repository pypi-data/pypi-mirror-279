# This file is placed in the Public Domain.


"init"


from nixt.run.main   import Cfg
from nixt.run.thread import launch
from nixt.run.utils  import getmods, spl


def ini(event):
    "run init on modules."
    if not event.args:
        event.reply("ini <name>")
        return
    mods = getmods(Cfg)
    if not mods:
        event.reply("modules are not available")
        return
    for name in event.args:
        for nme in spl(name):
            mod = getattr(mods, nme, None)
            if "init" in dir(mod):
                event.reply(f"launched {nme}")
                launch(mod.init)
