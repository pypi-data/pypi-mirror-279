#!/usr/bin/env python3
# This file is placed in the Public Domain.
#
# pylint: disable=E1102


"handler"


import inspect
import queue
import threading
import _thread


from nixt.lib.default import Default
from nixt.lib.object  import Object
from nixt.run.thread  import launch
from nixt.run.utils   import parse, spl


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


class Event(Default):

    "Event"

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self.result  = []
        self.txt     = ""
        self.type    = "command"

    def ready(self):
        "event is ready."
        self._ready.set()

    def reply(self, txt):
        "add text to the result"
        self.result.append(txt)

    def wait(self):
        "wait for event to be ready."
        self._ready.wait()
        return self.result


class Handler:

    "Handler"

    def __init__(self):
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True

    def callback(self, evt):
        "call callback based on event type."
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        func(self, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        "register callback for a type."
        setattr(self.cbs, typ, cbs)

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()


class CLI(Handler):

    "CLI"

    out = None

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        if self.out:
            txt = txt.encode('utf-8', 'replace').decode()
            self.out(txt)

    def show(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)


def cmnd(txt, outer):
    "do a command using the provided output function."
    cli = CLI()
    cli.out = outer
    evn = Event()
    evn.txt = txt
    command(cli, evn)
    evn.wait()
    return evn


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
        'Event',
        'Handler',
        'cmnd',
        'command',
        'scan'
    )
