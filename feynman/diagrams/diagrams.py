"""Diagram class"""

from copy import deepcopy
import warnings

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpa
import matplotlib.text as mpt

from .. import colors as mc
from .. import vectors
from .. import colors
from .. import core
from ..core import Vertex, Line, Operator

from .plotter import Plotter


class Diagram(Plotter):
    """
    The main object for a feynman diagram.

    Parameters
    ----------

    ax:
        A :class:`matplotlib.axes.AxesSubplot`  instance.
        If no ax is given, a new figure and a new axe are initialized.

    xy0:
        Default reference point for creation of vertices.

    transparent: :vartype: `bool`
        Set the background as transparent.

    """

    _scale = (1.0, 1.0)
    _transform = None

    def __init__(self, ax=None, xy0=(0.0, 0.0), **kwargs):
        super().__init__(ax=ax, **kwargs)

        self.line_length = 0.2
        self.operator_size = 1.5

        self.x0, self.y0 = xy0

        self.vertices = list()
        self.lines = list()
        self.operators = list()

    def vertex(self, xy=None, **kwargs):
        """
        Create a :class:`feynman.Vertex` vertex.

        Parameters
        ----------

        xy:
            Coordinates of the vertex.
        **kwargs:
            Any argument passed to :class:`feynman.Vertex`

        Returns
        -------
        :class:`feynman.Vertex`
        """

        if xy is None:
            xy = (self.x0, self.y0)

        v = Vertex(xy, **kwargs)
        self.add_vertex(v)

        return v

    def vertices(self, xys, **kwargs):
        """
        Create multiple vertices.

        Parameters
        ----------

        xys :
            List of xy coordinates.

        **kwargs :
            Any matplotlib line style argument.

        Returns
        -------
        list of feynman.Vertex instance.
        """

        xys = np.array(xys)
        if xys.ndim != 2:
            raise ValueError("xy must be a list of xy coordinates.")

        vs = list()
        for xy in xys:
            v = Vertex(xy, **kwargs)
            self.add_vertex(v)
            vs.append(v)
        return vs

    def line(self, *args, **kwargs):
        """
        Create :class:`feynman.Line` instance.
        """

        l = Line(*args, **kwargs)
        self.lines.append(l)
        return l

    def operator(self, *args, **kwargs):
        """
        Create :class:`feynman.Operator` instance.
        """

        o = Operator(*args, **kwargs)
        self.operators.append(o)
        return o

    def add_vertex(self, vertex):
        """
        Add feynman.Vertex instance.
        """

        vertex._diagram = self
        self.vertices.append(vertex)

    def add_line(self, line):
        """
        Add feynman.Line instance.
        """

        line._diagram = self
        self.lines.append(line)

    def add_operator(self, operator):
        """
        Add feynman.Operator instance.
        """

        operator.diagram = self
        self.operators.append(operator)
        for v in operator.vertices:
            # if v in self.vertices: continue  # Should avoid this check
            self.add_vertex(v)

    def plot(self):
        """
        Draw the diagram.
        """

        for v in self.vertices:
            v.draw(self.ax)

        for l in self.lines:
            l.draw(self.ax)

        for O in self.operators:
            O.draw(self.ax)

    # def plot(self, *args, **kwargs):
    #     return self.draw(*args, **kwargs)

    def add_chunk(self, vertex, dx=0, dy=0, angle=0, radius=0, **line_prop):
        """
        Create a chunk going to the vertex by initializing a vertex and a line.
        The new vertex will be invisible by default.
        All other keyword arguments are passed to the line.

        Return: new_vertex, new_line
        """

        v_prop = dict(dx=dx, dy=dy, angle=angle, radius=radius)
        v_prop.setdefault("marker", "")
        line_prop.setdefault("style", "simple single linear")
        line_prop.setdefault("arrow", False)
        v = self.vertex(vertex.xy, **v_prop)
        l = self.line(v, vertex, **line_prop)
        return v, l

    def text(self, *args, **kwargs):
        """Add text using matplotlib.axes.Axes.text."""

        kwargs.setdefault("ha", "center")
        kwargs.setdefault("va", "center")
        kwargs.setdefault("fontsize", 30)
        self.ax.text(*args, **kwargs)

    def scale(self, x):
        """
        Apply a scaling factor to the diagram.
        Suppose your diagram looks good for a figure of size (6, 6) with a single subplot.
        If you create multiple subplots in your figure,
        each with its own diagram (e.g. to represent an equation),
        then the same diagram will generally look too thick in the smaller subplots.
        It is then desirable to apply a scaling factor to thin down
        the lines, the arrows, and the text for all objects of the diagram.
        """

        for v in self.vertices:
            v.scale(x)

        for l in self.lines:
            l.scale(x)

        for o in self.operators:
            o.scale(x)

    # def get_object_group_limits():
    #    """
    #    Return the x0, y0, w, h
    #    of the leftmost, bottommost, rightmost and topmost objects.
    #    """
    #    raise NotImplementedError()
