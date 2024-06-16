# This file is placed in the Public Domain.


"list of commands."


from nixt.__main__ import Cfg


def ver(event):
    "list commands."
    event.reply(f"{Cfg.name.upper()} version {Cfg.version}")
