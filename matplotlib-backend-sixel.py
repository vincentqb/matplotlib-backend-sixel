# SPDX-License-Identifier: CC0-1.0

import sys
from tempfile import NamedTemporaryFile

from matplotlib import interactive, is_interactive
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase, _Backend
from matplotlib.backends.backend_agg import FigureCanvasAgg
from sixel.converter import SixelConverter

# XXX heuristic for interactive repl
if sys.flags.interactive:
    interactive(True)


class FigureManagerSixel(FigureManagerBase):
    def show(self):
        with NamedTemporaryFile() as temppng:
            self.canvas.figure.savefig(temppng.name, bbox_inches="tight", format="png")
            sixel_convert = SixelConverter(temppng)
            sixel_convert.write(sys.stdout)


class FigureCanvasSixel(FigureCanvasAgg):
    manager_class = FigureManagerSixel


@_Backend.export
class _BackendSixelAgg(_Backend):
    FigureCanvas = FigureCanvasSixel
    FigureManager = FigureManagerSixel

    # Noop function instead of None signals that this is an "interactive" backend
    def mainloop():
        return

    # XXX: `draw_if_interactive` isn't really intended for on-shot rendering.
    # We run the risk of being called on a figure that isn't completely rendered yet,
    # so we skip draw calls for figures that we detect as not being fully initialized yet.
    # Our heuristic for that is the presence of axes on the figure.
    @classmethod
    def draw_if_interactive(cls):
        manager = Gcf.get_active()
        if is_interactive() and manager.canvas.figure.get_axes():
            cls.show()

    @classmethod
    def show(cls, *args, **kwargs):
        _Backend.show(*args, **kwargs)
        Gcf.destroy_all()
