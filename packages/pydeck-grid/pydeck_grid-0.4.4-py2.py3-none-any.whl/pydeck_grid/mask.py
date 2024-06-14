import os
from .layer import GridLayerException
from pydeck.bindings.layer import Layer

MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")
MASK_URL = (
    "https://api.mapbox.com/v4/mapbox.country-boundaries-v1/{z}/{x}/{y}.vector.pbf?access_token="
    + MAPBOX_API_KEY
)


class MaskLayer(Layer):
    def __init__(self, mask_url=MASK_URL, id=None, **kwargs):
        """Configures a deck.gl masking layer for creating transparent cutouts. Useful for creating clean shorelines for ocean data.

        Args:
            mask_url : str, default "https://api.mapbox.com/v4/mapbox.country-boundaries-v1/{z}/{x}/{y}.vector.pbf?access_token={MAPBOX_API_KEY}"
                URL of the masking tileset. Must be a valid URL to a vector tile tileset following the same conventions as the deck.gl MVTLayer.
                All of the tileset's features will be used to mask the data layer.

            invert : bool, default False
                Invert the mask. Useful for masking land instead of water.


        Raises:
            GridLayerException
                missing or invalid arguments

        """

        super().__init__(type="MaskLayer", mask_url=mask_url, id=id, **kwargs)
