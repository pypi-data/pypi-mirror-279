#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydeck_grid` package."""
import os
import tempfile
import pytest
import pydeck as pdk
import xarray as xr


from pydeck_grid import PcolorLayer, ParticleLayer, MaskLayer


HERE = os.path.dirname(__file__)

MAP_TOKEN = os.environ.get("MAPBOX_API_KEY", "")


@pytest.fixture
def data():
    data = xr.open_dataset(os.path.join(HERE, "data", "gfs_test.nc"))
    return data.sel(longitude=slice(165, 180), latitude=slice(-48, -33))


@pytest.fixture
def view(data):
    view = pdk.ViewState(
        longitude=float(data.longitude.mean()),
        latitude=float(data.latitude.mean()),
        zoom=3,
        min_zoom=2,
        max_zoom=10,
        pitch=0,
        bearing=0,
    )
    return view


def test_pcolor_mask(data, view):
    datakeys = {"x": "longitude", "y": "latitude", "c": "TMP_2maboveground"}
    layer = PcolorLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=-40,
        vmax=40,
        offset=-273,
        pickable=True,
    )
    mask = MaskLayer()
    assert isinstance(mask, pdk.Layer)
    r = pdk.Deck(
        [layer, mask],
        initial_view_state=view,
        tooltip={
            "html": "<b>Temperature:</b> {value} °C",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        description=layer.colorbar(labels=[-40, -30, -20, -10, 0, 10, 20, 30, 40]),
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)
