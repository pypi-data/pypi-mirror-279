# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

from typing import Literal

import scipp as sc

from .. import backends
from ..core import View
from ..core.typing import FigureLike
from ..core.utils import make_compatible
from .camera import Camera
from .colormapper import ColorMapper


class Scatter3dView(View):
    """
    View that makes a visual representation of three-dimensional scatter data.
    It has a :class:`Canvas`, a :class:`ColorMapper` and a specialized ``update``
    function that generates :class:`PointCloud` artists.

    Parameters
    ----------
    *nodes:
        The nodes that are attached to the view.
    x:
        The name of the coordinate to use for the X positions of the scatter points.
    y:
        The name of the coordinate to use for the Y positions of the scatter points.
    z:
        The name of the coordinate to use for the Z positions of the scatter points.
    cmap:
        The name of the colormap for the data
        (see https://matplotlib.org/stable/tutorials/colors/colormaps.html).
        In addition to the Matplotlib docs, if the name is just a single html color,
        a colormap with that single color will be used.
    mask_cmap:
        The name of the colormap for masked data.
    norm:
        Control the scaling on the vertical axis.
    vmin:
        Lower bound for the colorbar. If a number (without a unit) is supplied, it is
        assumed that the unit is the same as the data unit.
    vmax:
        Upper bound for the colorbar. If a number (without a unit) is supplied, it is
        assumed that the unit is the same as the data unit.
    title:
        The figure title.
    figsize:
        The width and height of the figure, in pixels.
    camera:
        Initial camera configuration (position, target).
    **kwargs:
        All other kwargs are forwarded to the PointCloud artist.
    """

    def __init__(
        self,
        *nodes,
        x: str = 'x',
        y: str = 'y',
        z: str = 'z',
        cmap: str = 'viridis',
        mask_cmap: str = 'gray',
        norm: Literal['linear', 'log'] = 'linear',
        vmin: sc.Variable | float | None = None,
        vmax: sc.Variable | float | None = None,
        figsize: tuple[int, int] = (600, 400),
        title: str | None = None,
        camera: Camera | None = None,
        **kwargs,
    ):
        super().__init__(*nodes)

        self._x = x
        self._y = y
        self._z = z
        self._kwargs = kwargs

        self.canvas = backends.canvas3d(figsize=figsize, title=title, camera=camera)
        self.colormapper = ColorMapper(
            cmap=cmap,
            mask_cmap=mask_cmap,
            norm=norm,
            vmin=vmin,
            vmax=vmax,
            nan_color="#f0f0f0",
            figsize=self.canvas.figsize,
        )

        self._original_artists = [n.id for n in nodes]
        self.render()

    def update(self, *args, **kwargs):
        """
        Update the view with new point clouds by either supplying a dictionary of
        new data or by keyword arguments.
        """
        new = dict(*args, **kwargs)
        mapping = {'x': self._x, 'y': self._y, 'z': self._z}
        for key, new_values in new.items():
            if self.canvas.empty:
                self.canvas.set_axes(
                    dims=mapping,
                    units={
                        x: new_values.coords[dim].unit for x, dim in mapping.items()
                    },
                    dtypes={
                        x: new_values.coords[dim].dtype for x, dim in mapping.items()
                    },
                )
                self.colormapper.unit = new_values.unit
            else:
                new_values.data = make_compatible(
                    new_values.data, unit=self.colormapper.unit
                )
                for xyz, dim in mapping.items():
                    new_values.coords[dim] = new_values.coords[dim].to(
                        unit=self.canvas.units[xyz], copy=False
                    )

            if key not in self.artists:
                pts = backends.point_cloud(
                    data=new_values, x=self._x, y=self._y, z=self._z, **self._kwargs
                )
                self.artists[key] = pts
                self.colormapper[key] = pts
                self.canvas.add(pts.points)
                if key in self._original_artists:
                    self.canvas.make_outline(limits=self.get_limits())

            self.artists[key].update(new_values=new_values)
        self.colormapper.update(**new)

    def get_limits(self) -> tuple[sc.Variable, sc.Variable, sc.Variable]:
        """
        Get global limits for all the point clouds in the scene.
        """
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        zmin = None
        zmax = None
        for child in self.artists.values():
            xlims, ylims, zlims = child.get_limits()
            if xmin is None or xlims[0] < xmin:
                xmin = xlims[0]
            if xmax is None or xlims[1] > xmax:
                xmax = xlims[1]
            if ymin is None or ylims[0] < ymin:
                ymin = ylims[0]
            if ymax is None or ylims[1] > ymax:
                ymax = ylims[1]
            if zmin is None or zlims[0] < zmin:
                zmin = zlims[0]
            if zmax is None or zlims[1] > zmax:
                zmax = zlims[1]
        return (
            sc.concat([xmin, xmax], dim=self._x),
            sc.concat([ymin, ymax], dim=self._y),
            sc.concat([zmin, zmax], dim=self._z),
        )

    def set_opacity(self, alpha: float):
        """
        Update the opacity of the original children (not the cuts).

        Parameters
        ----------
        alpha:
            The opacity value, between 0 and 1.
        """
        for name in self._original_artists:
            self.artists[name].opacity = alpha

    def remove(self, key: str):
        """
        Remove an object from the scene.

        Parameters
        ----------
        key:
            The id of the object to be removed.
        """
        self.canvas.remove(self.artists[key].points)
        del self.artists[key]


def scatter3dfigure(*args, **kwargs) -> FigureLike:
    """
    Create a figure to represent three-dimensional data from one or more graph node(s).

    .. versionadded:: 24.04.0

    Examples
    --------
    Create an input node and attach a ``scatter3dfigure`` as a view:

      >>> da = pp.data.scatter()
      >>> in_node = pp.Node(da)
      >>> fig = pp.scatter3dfigure(in_node)

    With a customization argument to make the color scale logarithmic:

      >>> da = pp.data.scatter()
      >>> in_node = pp.Node(da)
      >>> fig = pp.scatter3dfigure(in_node, norm='log')
    """

    return backends.figure3d(Scatter3dView, *args, **kwargs)
