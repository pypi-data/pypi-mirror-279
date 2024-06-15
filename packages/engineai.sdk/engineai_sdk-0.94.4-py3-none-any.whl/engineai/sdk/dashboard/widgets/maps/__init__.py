"""Map resources."""

from .color_axis import ColorAxis
from .enums import LegendPosition
from .enums import Region
from .geo.geo import Geo
from .geo.styling.label import MapStylingLabel
from .geo.styling.styling import MapStyling
from .series.numeric import NumericSeries
from .series.styling import SeriesStyling

__all__ = [
    # .geo
    "Geo",
    "Region",
    # .position
    "LegendPosition",
    # .series
    "NumericSeries",
    # .seriesStyling
    "SeriesStyling",
    # .color_axis"
    "ColorAxis",
    # .styling
    "MapStyling",
    "MapStylingLabel",
]
