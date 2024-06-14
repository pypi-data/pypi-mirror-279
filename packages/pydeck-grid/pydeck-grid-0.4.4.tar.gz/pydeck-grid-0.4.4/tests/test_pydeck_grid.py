#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydeck_grid` package."""
import os
import tempfile
import pytest
import pydeck as pdk
import xarray as xr


from pydeck_grid import PcolorLayer, ParticleLayer, PartmeshLayer, GContourLayer


HERE = os.path.dirname(__file__)


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


def test_pcolor_scalar(data, view):
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
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip={
            "html": "<b>Temperature:</b> {value} °C",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        description=layer.colorbar(labels=[-40, -30, -20, -10, 0, 10, 20, 30, 40]),
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_pcolor_vector(data, view):
    datakeys = {
        "x": "longitude",
        "y": "latitude",
        "u": "UGRD_10maboveground",
        "v": "VGRD_10maboveground",
    }
    layer = PcolorLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=50,
        scale=1.92,
        pickable=True,
        precision=2,
    )
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip={
            "html": "<b>Windspeed:</b> {value} kts",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_particles_vector(data, view):
    datakeys = {
        "x": "longitude",
        "y": "latitude",
        "u": "UGRD_10maboveground",
        "v": "VGRD_10maboveground",
    }
    layer = ParticleLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=50,
        scale=1.92,
    )
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip=True,
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_partmesh_vector(data, view):
    datakeys = {
        "x": "longitude",
        "y": "latitude",
        "u": "UGRD_10maboveground",
        "v": "VGRD_10maboveground",
    }
    layer = PartmeshLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=50,
        scale=1.92,
        mesh={"shape": "quiver"},
    )
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip=True,
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_contour_scalar(data, view):
    datakeys = {
        "x": "longitude",
        "y": "latitude",
        "c": "TMP_2maboveground",
    }
    layer = GContourLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=-40,
        vmax=40,
        offset=-273,
        color="#FFFFFF",
        levels=[-40, -30, -20, -10, 0, 5, 10, 15, 20, 25, 30, 40],
    )
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip=True,
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_multi_layer(data, view):
    datakeys = {
        "x": "longitude",
        "y": "latitude",
        "u": "UGRD_10maboveground",
        "v": "VGRD_10maboveground",
    }
    layer1 = PartmeshLayer(
        data,
        datakeys,
        id="test1",
        color="#FFFFFF",
        altitude=100,
        mesh={"shape": "quiver"},
    )
    layer2 = PcolorLayer(
        data,
        datakeys,
        id="test2",
        colormap="turbo",
        vmin=0,
        vmax=50,
        scale=1.92,
        opacity=0.5,
    )
    r = pdk.Deck(
        [layer2, layer1],
        initial_view_state=view,
        tooltip=True,
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)
