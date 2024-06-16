# This file is placed in the Public Domain.


"locate"


from nixt.lib.object  import fmt
from nixt.run.persist import Persist


def fnd(event):
    "locate objects."
    Persist.skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in Persist.types()])
        if res:
            event.reply(",".join(res))
        return
    otype = Persist.long(event.args[0])
    nmr = 0
    for _fnm, obj in Persist.find(otype, event.gets):
        event.reply(f"{nmr} {fmt(obj)}")
        nmr += 1
    if not nmr:
        event.reply("no result")
