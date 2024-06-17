# Claudio Perez
import numpy as np
from .canvas import Canvas
from ..views import VIEWS

class MatplotlibCanvas(Canvas):
    def __init__(self, ndm=3, ax=None):

        self.ndm = ndm

        import matplotlib.pyplot as plt
        self.plt = plt
        if ax is None:
            _, ax = plt.subplots(1, 1, subplot_kw={"projection": "3d"})
            ax.set_autoscale_on(True)
            ax.set_axis_off()

        self.ax = ax

    def show(self):
        self.plt.show()

    def build(self):
        ax = self.ax
        opts = self.config
        aspect = [ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz'[:self.ndm])]
        aspect = [max(a,max(aspect)/8) for a in aspect]
        if self.ndm == 3:
            ax.set_box_aspect(aspect)#, zoom=3)
            ax.view_init(**VIEWS[opts["view"]])
        else:
            ax.set_aspect("equal") #set_box_aspect(1)#, zoom=3)
        return ax

    def write(self, filename=None):
        self.ax.figure.savefig(self.config["write_file"])

    def plot_lines(self, coords, label=None, conf=None, color=None):
        props = conf or {"color": color or "grey", "alpha": 0.6, "linewidth": 0.5}
        self.ax.plot(*coords.T, **props)

    def plot_nodes(self, coords, label=None, conf=None, data=None):
        ax = self.ax
        props = {"color": "black",
                 "marker": "s",
                 "s": 0.1,
                 "zorder": 2
        }
        self.ax.scatter(*coords.T, **props)

    def plot_vectors(self, locs, vecs, alr=0.1, **kwds):
        self.ax.quiver(*locs, *vecs, arrow_length_ratio=alr, color="black")

    def plot_trisurf(self, xyz, ijk):
        ax.plot_trisurf(*xyz.T, triangles=ijk)



