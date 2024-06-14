#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydeck_grid` package."""
import os
import tempfile
import pytest
import pydeck as pdk
import xarray as xr


from pydeck_grid import ImageLayer


HERE = os.path.dirname(__file__)


@pytest.fixture
def data():
    data = xr.open_dataset(
        os.path.join(HERE, "data", "chart_image.nc"), mask_and_scale=False
    )
    return data.isel(x=slice(None, None, 10), y=slice(None, None, 10))


@pytest.fixture
def view(data):
    view = pdk.ViewState(
        longitude=float(data.x.mean()),
        latitude=float(data.y.mean()),
        zoom=10,
        min_zoom=2,
        max_zoom=12,
        pitch=0,
        bearing=0,
    )
    return view


def test_image(data, view):
    datakeys = {"x": "x", "y": "y", "b": "band", "c": "band_data"}
    layer = ImageLayer(data, datakeys, id="test")
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip=True,
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)
