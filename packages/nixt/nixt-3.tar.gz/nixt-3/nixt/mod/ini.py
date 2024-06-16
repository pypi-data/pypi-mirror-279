# This file is placed in the Public Domain.


"init"


from nixt.run.thread import launch
from nixt.run.utils  import spl


try:
    import mods as MODS
except ModuleNotFoundError:
    MODS = None


def ini(event):
    "run init on modules."
    if not event.args:
        event.reply("ini <name>")
        return
    if not MODS:
        event.reply("modules not availabl")
        return
    for name in event.args:
        for nme in spl(name):
            mod = getattr(MODS, nme, None)
            if "init" in dir(mod):
                event.reply(f"launched {nme}")
                launch(mod.init)
 