# This file is placed in the Public Domain.
#
#


"at repeating intervals"


from nixt.run.thread import launch
from nixt.run.timer  import Timer


class Repeater(Timer):

    "Repeater"

    def run(self):
        launch(self.start)
        super().run()


def __dir__():
    return (
        'Repeater',
    )
