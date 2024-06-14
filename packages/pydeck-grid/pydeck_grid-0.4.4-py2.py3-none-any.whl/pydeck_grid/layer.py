import orjson

import xarray as xr
import numpy as np
from matplotlib.colors import rgb2hex, hex2color
from pydeck.bindings.layer import Layer
from pydeck.types.base import PydeckType
from pydeck.bindings.json_tools import JSONMixin, IGNORE_KEYS, lower_camel_case_keys

import pydeck

from .colormap import GridColormap
from .legend import Colorbar

pydeck.settings.custom_libraries = pydeck.settings.custom_libraries + [
    {
        "libraryName": "DeckGriddedLayers",
        "resourceUri": "https://assets.oceanum.io/packages/deck-gl-grid/bundle.umd.cjs",
    }
]


def sanitize_color(color):
    if isinstance(color, str):
        if color.startswith("#"):
            color = [255 * c for c in hex2color(color)]
    return color


# Patch pydeck to use orjson for numpy arrays
def default_serialize(o, remap_function=lower_camel_case_keys):
    """Default method for rendering JSON from a dictionary"""
    if issubclass(type(o), PydeckType):
        return repr(o)
    elif isinstance(o, np.ndarray):
        if o.ndim:
            return o.tolist()
        else:
            return o.item()
    attrs = vars(o)
    attrs = {k: v for k, v in attrs.items() if v is not None}
    for ignore_attr in IGNORE_KEYS:
        if attrs.get(ignore_attr):
            del attrs[ignore_attr]
    if remap_function:
        remap_function(attrs)
    return attrs


def orjson_serializer(serializable):
    return orjson.dumps(
        serializable,
        option=orjson.OPT_SERIALIZE_NUMPY,
        default=default_serialize,
    ).decode("utf-8")


JSONMixin.to_json = orjson_serializer


class GridLayerData(dict):
    def __init__(self, data, datakeys):
        _data = {"coords": {}, "data_vars": {}}
        for v in datakeys.values():
            if v in data.coords:
                arr = data.coords[v].values
                if not arr.data.contiguous:
                    arr = np.ascontiguousarray(arr)
                _data["coords"][v] = {"data": arr}
            else:
                _data["data_vars"][v] = {"data": data.data_vars[v].values}
        super().__init__(_data)


class GridLayerException(Exception):
    pass


class GridLayer(Layer):
    """Base layer for all pydeck grid layers"""

    def __init__(
        self,
        type,
        data,
        datakeys,
        id=None,
        colormap=None,
        vmin=0.0,
        vmax=1.0,
        **kwargs,
    ):
        """Configures a deck.gl layer for rendering gridded data on a map. Parameters passed
        here will be specific to the particular deck.gl grid layer that you are choosing to use.
        """

        self.grid_colormap = GridColormap(colormap, vmin, vmax) if colormap else None

        if kwargs.get("visible", True):
            if not isinstance(data, xr.Dataset):
                raise GridLayerException("Data must be an xarray DataSet")
            if datakeys["x"] not in data.variables:
                raise GridLayerException(f"x coordinate {datakeys['x']} not in data")
            if datakeys["y"] not in data.variables:
                raise GridLayerException(f"y coordinate {datakeys['y']} not in data")
            if len(data.variables[datakeys["x"]].dims) > 1:
                raise GridLayerException(f"x coordinate {datakeys['x']} is not 1D")
            if len(data.variables[datakeys["y"]].dims) > 1:
                raise GridLayerException(f"y coordinate {datakeys['y']} is not 1D")

            gridded = datakeys["x"] in data.coords and datakeys["y"] in data.coords

            coord_dims = set(
                data.variables[datakeys["x"]].dims + data.variables[datakeys["y"]].dims
            )

            # Take first 2D grid from the data array
            ndims = len(data.dims)
            if gridded and ndims < 2:
                raise GridLayerException("Gridded layer data must be at least 2D")
            indexer = {
                i: 0
                for i in data.dims
                if i not in list(coord_dims) + ["b" in datakeys and datakeys["b"]]
            }
            griddata = GridLayerData(data.isel(**indexer, drop=True), datakeys)
        else:
            griddata = None

        super().__init__(
            type,
            griddata,
            id,
            use_binary_transport=False,
            colormap=self.grid_colormap,
            datakeys=datakeys,
            **kwargs,
        )

    def colorbar(
        self,
        labels=None,
        units=None,
        width=200,
        height=40,
        labelcolor="white",
        style=None,
    ):
        """Return a colorbar for the layer to use in the pydeck description

        Args:
            labels: list, optional
                List of labels to use for the colorbar
            units: str, optional
                Units string to use for the colorbar
            width: int, optional
                Width of the colorbar in pixels
            height: int, optional
                Height of the colorbar in pixels
            labelcolor: str, optional
                Color of the colorbar labels
            style: dict, optional
                Additional style properties to apply to the colorbar
        """
        colorbar_instance = Colorbar(
            self.grid_colormap,
            labels=labels,
            units=units,
        )
        return colorbar_instance.to_html(
            width=width,
            height=height,
            labelcolor=labelcolor,
            style=style or {},
        )
