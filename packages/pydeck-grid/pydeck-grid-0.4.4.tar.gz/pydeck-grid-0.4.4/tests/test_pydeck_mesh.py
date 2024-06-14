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
    data = xr.open_dataset(os.path.join(HERE, "data", "mesh_test.nc"))
    return data


@pytest.fixture
def view(data):
    view = pdk.ViewState(
        longitude=float(data.lon.mean()),
        latitude=float(data.lat.mean()),
        zoom=12,
        min_zoom=2,
        max_zoom=14,
        pitch=0,
        bearing=0,
    )
    return view


def test_pcolor_vector(data, view):
    datakeys = {
        "x": "lon",
        "y": "lat",
        "u": "us",
        "v": "vs",
    }
    layer = PcolorLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=2,
        scale=1.92,
        pickable=True,
        precision=2,
    )
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        views=[pdk.View(type="MapView", controller=True, repeat=True)],
        initial_view_state=view,
        tooltip={
            "html": "<b>Current speed:</b> {value} kts",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        description=layer.colorbar(
            labels=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0],
            units="kts",
            width=400,
            height=50,
        ),
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_particles_vector(data, view):
    datakeys = {
        "x": "lon",
        "y": "lat",
        "u": "us",
        "v": "vs",
    }
    layer1 = PcolorLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=2,
        scale=1.92,
        pickable=True,
        precision=2,
        opacity=0,
    )
    layer2 = ParticleLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=2,
        scale=1.92,
    )
    assert isinstance(layer1, pdk.Layer)
    r = pdk.Deck(
        [layer1, layer2],
        initial_view_state=view,
        tooltip={
            "html": "<b>Current speed:</b> {value} kts",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        description=layer2.colorbar(
            labels=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0],
            units="kts",
            width=400,
            height=50,
        ),
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_partmesh_vector(data, view):
    datakeys = {
        "x": "lon",
        "y": "lat",
        "u": "us",
        "v": "vs",
    }
    layer = PartmeshLayer(
        data,
        datakeys,
        id="test",
        colormap="turbo",
        vmin=0,
        vmax=2,
        scale=1.92,
        npart=100,
        mesh={"shape": "quiver"},
    )
    assert isinstance(layer, pdk.Layer)
    r = pdk.Deck(
        layer,
        initial_view_state=view,
        tooltip={
            "html": "<b>Current speed:</b> {value} kts",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        description=layer.colorbar(
            labels=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0],
            units="kts",
            width=400,
            height=50,
        ),
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)


def test_multi_layer(data, view):
    datakeys = {
        "x": "lon",
        "y": "lat",
        "u": "us",
        "v": "vs",
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
        vmax=2,
        scale=1.92,
        opacity=0.5,
    )
    r = pdk.Deck(
        [layer2, layer1],
        initial_view_state=view,
        tooltip={
            "html": "<b>Current speed:</b> {value} kts",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        description=layer2.colorbar(
            labels=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0],
            units="kts",
            width=400,
            height=50,
        ),
    )
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)
