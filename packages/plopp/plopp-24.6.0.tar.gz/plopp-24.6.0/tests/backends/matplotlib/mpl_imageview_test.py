# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

import matplotlib.pyplot as plt
import numpy as np
import scipp as sc

from plopp import Node
from plopp.data.testing import data_array
from plopp.graphics.imageview import ImageView


def test_cbar():
    da = data_array(ndim=2, binedges=True)
    fig = ImageView(Node(da), cbar=False)
    assert fig.canvas.cax is None


def test_update_on_one_mesh_changes_colors_on_second_mesh():
    da1 = data_array(ndim=2)
    da2 = 3.0 * data_array(ndim=2)
    da2.coords['xx'] += sc.scalar(50.0, unit='m')
    a = Node(da1)
    b = Node(da2)
    f = ImageView(a, b)
    old_b_colors = f.artists[b.id]._mesh.get_facecolors()
    a.func = lambda: da1 * 2.1
    a.notify_children('updated a')
    # No change because the update did not change the colorbar limits
    assert np.allclose(old_b_colors, f.artists[b.id]._mesh.get_facecolors())
    a.func = lambda: da1 * 5.0
    a.notify_children('updated a')
    assert not np.allclose(old_b_colors, f.artists[b.id]._mesh.get_facecolors())


def test_with_string_coord():
    strings = ['a', 'b', 'c', 'd', 'e']
    da = sc.DataArray(
        data=sc.array(dims=['y', 'x'], values=np.random.random((5, 5))),
        coords={
            'x': sc.array(dims=['x'], values=strings, unit='s'),
            'y': sc.arange('y', 5.0, unit='m'),
        },
    )
    fig = ImageView(Node(da))
    assert [t.get_text() for t in fig.canvas.ax.get_xticklabels()] == strings


def test_with_strings_as_bin_edges():
    strings = ['a', 'b', 'c', 'd', 'e', 'f']
    da = sc.DataArray(
        data=sc.array(dims=['y', 'x'], values=np.random.random((5, 5))),
        coords={
            'x': sc.array(dims=['x'], values=strings, unit='s'),
            'y': sc.arange('y', 6.0, unit='m'),
        },
    )
    fig = ImageView(Node(da))
    assert [t.get_text() for t in fig.canvas.ax.get_xticklabels()] == strings


def test_with_strings_as_bin_edges_other_coord_is_bin_centers():
    strings = ['a', 'b', 'c', 'd', 'e', 'f']
    da = sc.DataArray(
        data=sc.array(dims=['y', 'x'], values=np.random.random((5, 5))),
        coords={
            'x': sc.array(dims=['x'], values=strings, unit='s'),
            'y': sc.arange('y', 5.0, unit='m'),
        },
    )
    fig = ImageView(Node(da))
    assert [t.get_text() for t in fig.canvas.ax.get_xticklabels()] == strings


def test_kwargs_are_forwarded_to_artist():
    da = data_array(ndim=2)
    fig = ImageView(Node(da), rasterized=True)
    [artist] = fig.artists.values()
    assert artist._mesh.get_rasterized()
    fig = ImageView(Node(da), rasterized=False)
    [artist] = fig.artists.values()
    assert not artist._mesh.get_rasterized()


def test_figsize():
    da = data_array(ndim=2)
    size = (8.1, 8.3)
    fig = ImageView(Node(da), figsize=size)
    assert np.allclose(fig.canvas.fig.get_size_inches(), size)


def test_grid():
    da = data_array(ndim=2)
    fig = ImageView(Node(da), grid=True)
    assert fig.canvas.ax.xaxis.get_gridlines()[0].get_visible()


def test_ax():
    fig, ax = plt.subplots()
    assert len(ax.collections) == 0
    da = data_array(ndim=2)
    _ = ImageView(Node(da), ax=ax)
    assert len(ax.collections) == 1


def test_cax():
    fig, ax = plt.subplots()
    cax = fig.add_axes([0.9, 0.02, 0.05, 0.98])
    assert len(cax.collections) == 0
    da = data_array(ndim=2)
    _ = ImageView(Node(da), ax=ax, cax=cax)
    assert len(cax.collections) > 0
