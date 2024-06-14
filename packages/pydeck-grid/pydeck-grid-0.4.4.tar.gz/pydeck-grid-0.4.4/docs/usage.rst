=====
Usage
=====

To use pydeck-grid in a project::

    import tempfile
    import pydeck as pdk
    import xarray as xr
    import pydeck_grid
    from pydeck_grid import PcolorLayer

    #This is some sample data included with the library
    import urllib.request
    url="https://github.com/oceanum-io/pydeck-grid/raw/main/tests/data/gfs_test.nc"
    filename, headers = urllib.request.urlretrieve(url)
    data=xr.open_dataset(filename)

    view = pdk.ViewState(
        longitude=float(data.longitude.mean()),
        latitude=float(data.latitude.mean()),
        zoom=3,
        min_zoom=2,
        max_zoom=10,
        pitch=0,
        bearing=0,
    )

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


The ``data`` argument is always a xarray Dataset which must have coordinates or data variables corresponding to the datakeys argument.

The ``x``, ``y`` and ``z`` coordinates must be one dimensional. If the data variables have additional dimensions, the first member of each other dimension will be used.

You can use unstructured grids where the coordinates are provided for each point in the grid and must share a common grid node dimension. The data variables must have the same dimension as the coordinates and as with regular gridded datasets, the first member of each other dimension will be used. 

This is an example of a unstructured grid::

    import tempfile
    import pydeck as pdk
    import xarray as xr
    import pydeck_grid
    from pydeck_grid import ParticleLayer

    #This is some sample data included with the library
    import urllib.request
    url="https://github.com/oceanum-io/pydeck-grid/raw/main/tests/data/mesh_test.nc"
    filename, headers = urllib.request.urlretrieve(url)
    data=xr.open_dataset(filename)

    view = pdk.ViewState(
        longitude=float(data.longitude.mean()),
        latitude=float(data.latitude.mean()),
        zoom=12,
        min_zoom=2,
        max_zoom=18,
        pitch=0,
        bearing=0,
    )

    datakeys = {
        "x": "lon",
        "y": "lat",
        "u": "us",
        "v": "vs",
    }

    layer1 = PcolorLayer(
        data,
        datakeys,
        id="test1",
        opacity=0.,
        scale=1.92,
        pickable=True,
        precision=2,
    )

    layer2 = ParticleLayer(
        data,
        datakeys,
        id="test2",
        colormap="turbo",
        vmin=0,
        vmax=2,
        scale=1.92,
        precision=2,
    )
    
    r = pdk.Deck(
        [layer1,layer2],
        initial_view_state=view,
        tooltip={
            "html": "<b>Current speed:</b> {value} kts",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    )
    
    fname = tempfile.mktemp(suffix=".html")
    r.to_html(fname, True)

Note that a transparent PcolorLayer has been used to provide the mouseover tooltips.