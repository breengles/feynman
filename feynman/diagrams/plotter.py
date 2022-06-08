import os
import matplotlib.pyplot as plt

from numpy import array


class Plotter:
    """
    A wrapper for matplotlib.figure.Figure object.
    """

    def __init__(self, ax=None, **kwargs):
        """
        Init internal figure object.
        """

        # Init diagram and ax
        if ax is not None:
            self.ax = ax
            self.fig = ax.get_figure()
        else:
            self.fig = plt.figure()
            self.ax = self.fig.add_axes([0.0, 0.0, 1.0, 1.0])
            self.set_size_inches(*kwargs.get("figsize", (6, 6)))
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            for spine in self.ax.spines.values():
                spine.set_visible(False)

        self.set_ticks = kwargs.get("set_ticks", True)

        if self.set_ticks:
            self.ax.set_xticks([])
            self.ax.set_yticks([])

        self.transparent_background = kwargs.get("transparent", False)

        self.x0 = 0.0
        self.y0 = 0.0

    def show(self):
        """
        Show the figure with matplotlib.pyplot.show.
        """

        self.fig.show()

    def get_fig(self):
        """
        Get the figure.
        """

        return self.fig

    def get_axis(self):
        """
        Get the axe.
        """

        return self.ax

    def save(self, filepath, transparent=False):
        """
        Save a single figure
        """

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.fig.savefig(filepath, transparent=transparent)

    def set_size_inches(self, w=8, h=6):
        """
        Set the figure size, and set xlim, ylim, x0 and y0 accordingly.
        """

        # Geometry
        aspectratio = float(h) / float(w)
        self.fig.set_size_inches(w, h)

        self.ax.set_xlim(0.0, w)

        # self.ax.set_xlim(.0, 10.)
        self.ax.set_ylim(array(self.ax.get_xlim()) * aspectratio)
        self.y0 = sum(self.ax.get_ylim()) / 2.0
        self.x0 = sum(self.ax.get_xlim()) * 0.05
