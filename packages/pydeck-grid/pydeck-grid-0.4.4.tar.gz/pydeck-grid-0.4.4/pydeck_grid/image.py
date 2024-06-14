from .layer import GridLayer, GridLayerException


class ImageLayer(GridLayer):
    def __init__(
        self,
        data,
        datakeys={"x": "x", "y": "y", "b": "band", "c": "band_data"},
        id=None,
        opacity=1.0,
        altitude=0.0,
        zscale=1.0,
        global_wrap=False,
        **kwargs,
    ):
        """Configures a deck.gl image layer for rendering gridded image data. This layer only supports rectilinear grids.

        Args:
            data : xarray.DataSet
                Data to be visualized
            datakeys: dict,
                Dictionary of data keys to be used for the grid with keys:
                'x': x coordinate of the grid
                'y': y coordinate of the grid
                'b': band coordinate of the grid
                'z': z coordinate of the grid (optional)
                'c': scalar pixel value of the color band
                or
                'u': u component of the vector field
                'v': v component of the vector field
            id : str, default None
                Unique name for layer
            opacity: float, default 1.0,
                Opacity of the layer
            altitude: float, default 0.0
                Base altitude of layer in meters
            zscale: float, default 1.0
                Multiplier scale for the vertical level of the layer
            global_wrap: bool, default False
                Boolean indicating whether the grid is global and should be wrapped around the globe
            **kwargs: dict
                Additional keyword arguments for the deck.gl layer

        Raises:
            GridLayerException
                missing or invalid arguments

        """
        if kwargs.get("visible", True):
            if "b" in datakeys and "c" in datakeys:
                if datakeys["b"] not in data:
                    raise GridLayerException(
                        f"Band coordinate {datakeys['b']} not in data"
                    )
                if datakeys["c"] not in data:
                    raise GridLayerException(f"Pixel data {datakeys['c']} not in data")
            else:
                raise GridLayerException("datakeys must contain 'b' and 'c' keys")

        super().__init__(
            type="ImageLayer",
            data=data,
            id=id,
            opacity=opacity,
            altitude=altitude,
            zscale=zscale,
            global_wrap=global_wrap,
            datakeys=datakeys,
            pickable=False,
        )
