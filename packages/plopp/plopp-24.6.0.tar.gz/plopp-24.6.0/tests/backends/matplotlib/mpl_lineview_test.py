# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

import matplotlib.pyplot as plt
import numpy as np
import scipp as sc

from plopp import Node
from plopp.data.testing import data_array
from plopp.graphics.lineview import LineView


def test_with_string_coord():
    strings = ['a', 'b', 'c', 'd', 'e']
    da = sc.DataArray(
        data=sc.arange('x', 5.0),
        coords={'x': sc.array(dims=['x'], values=strings, unit='m')},
    )
    fig = LineView(Node(da))
    assert [t.get_text() for t in fig.canvas.ax.get_xticklabels()] == strings


def test_with_strings_as_bin_edges():
    strings = ['a', 'b', 'c', 'd', 'e', 'f']
    da = sc.DataArray(
        data=sc.arange('x', 5.0),
        coords={'x': sc.array(dims=['x'], values=strings, unit='m')},
    )
    fig = LineView(Node(da))
    assert [t.get_text() for t in fig.canvas.ax.get_xticklabels()] == strings


def test_figsize():
    da = data_array(ndim=1)
    size = (6.1, 3.3)
    fig = LineView(Node(da), figsize=size)
    assert np.allclose(fig.canvas.fig.get_size_inches(), size)


def test_grid():
    da = data_array(ndim=1)
    fig = LineView(Node(da), grid=True)
    assert fig.canvas.ax.xaxis.get_gridlines()[0].get_visible()


def test_ax():
    _, ax = plt.subplots()
    assert len(ax.lines) == 0
    da = data_array(ndim=1)
    _ = LineView(Node(da), ax=ax)
    assert len(ax.lines) > 0
