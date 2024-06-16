# This file is placed in the Public Domain.
#
# pylint: disable=R0903,E1103

"logging"


class Logging:

    "Logging"

    filter = []


def debug(txt):
    "print to console."
    for skp in Logging.filter:
        if skp in txt:
            return
    print(txt)


def __dir__():
    return (
        'Logging',
        'debug',
        'enable'
    )
