from .layer import GridLayer, GridLayerException, sanitize_color


class GContourLayer(GridLayer):
    def __init__(
        self,
        data,
        datakeys,
        id=None,
        opacity=1.0,
        altitude=0.0,
        zscale=1.0,
        global_wrap=False,
        color="#999999",
        colormap="turbo",
        scale=1.0,
        offset=0.0,
        vmin=0.0,
        vmax=1.0,
        levels=[],
        linewidth=1,
        **kwargs,
    ):
        """Configures a deck.gl contour layer for rendering gridded data. This layer only supports rectilinear grids.

        Args:
            data : xarray.DataSet
                Data to be visualized
            datakeys: dict,
                Dictionary of data keys to be used for the grid with keys:
                'x': x coordinate of the grid
                'y': y coordinate of the grid
                'z': z coordinate of the grid (optional)
                'c': scalar value of the grid
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
            color: str, default '#999999'
                Uniform color of contour lines
            colormap: str or matplotlib.cm.ScalarMappable, default 'turbo'
                Colormap to use for the grid as a matplotlib predefined colormap name or a matplotlib ScalarMappable
            vmin: float, default 0.0
                Minimum value for the colormap (if colormap is a matplotlib colormap name)
            vmax: float, default 1.0
                Maximum value for the colormap (if colormap is a matplotlib colormap name)
            scale: float, default 1.0
                Multiplier scale for the values of the grid
            offset: float, default 0.0
                Offset for the values in the grid
            levels: list, default []
                List of contour levels to draw
            linewidth: float, default 1
                Width of the contour lines

        Raises:
            GridLayerException
                missing or invalid arguments
        """

        if "c" in datakeys:
            if datakeys["c"] not in data:
                raise GridLayerException(f"scalar value {datakeys['c']} not in data")
        elif "u" in datakeys:
            if datakeys["u"] not in data or datakeys["v"] not in data:
                raise GridLayerException(
                    f"vector values {datakeys['u']},{datakeys['v']} not in data"
                )
        else:
            raise GridLayerException("datakeys must contain either 'c' or 'u' and 'v'")

        super().__init__(
            type="GContourLayer",
            data=data,
            id=id,
            opacity=opacity,
            altitude=altitude,
            zscale=zscale,
            global_wrap=global_wrap,
            color=sanitize_color(color),
            colormap=colormap,
            scale=scale,
            offset=offset,
            datakeys=datakeys,
            vmin=vmin,
            vmax=vmax,
            levels=levels,
            pickable=False,
            **kwargs,
        )
