"""Spec for Map Geo widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.maps.color_axis import ColorAxis
from engineai.sdk.dashboard.widgets.maps.enums import LegendPosition
from engineai.sdk.dashboard.widgets.maps.enums import Region

from ...base import WidgetTitleType
from ..series.series import MapSeries
from .base import BaseMapGeo
from .styling.styling import MapStyling


class Geo(BaseMapGeo[pd.DataFrame]):
    """Widget for tailored geographic data visualization.

    Allows the construction of a widget specifically tailored
    for geographical data visualization.
    """

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        series: Optional[MapSeries] = None,
        region_column: str = "region",
        color_axis: Optional[ColorAxis] = None,
        widget_id: Optional[str] = None,
        title: Optional[WidgetTitleType] = None,
        legend_position: LegendPosition = LegendPosition.BOTTOM,
        styling: Optional[MapStyling] = None,
        region: Region = Region.WORLD,
        tooltips: Optional[TooltipItems] = None,
    ):
        """Constructor for Map Geo widget.

        Args:
            data: data source for the widget.
            series: Series to be added to y axis.
            region_column: key to match region code in DS.
            widget_id: unique widget id in a dashboard.
            color_axis: color axis spec.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetField.
            legend_position: location of position relative to data, maps.
            styling: styling for the map.
            region: sets the region os the Map.
            tooltips: tooltip items to be displayed at Chart level.

        Examples:
            ??? example "Create a minimal Map widget"
                ```python linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import maps
                data = pd.DataFrame(
                    data=[
                        {"region": "PT", "value": 10, "tooltip": "A"},
                        {"region": "GB", "value": 100, "tooltip": "B"},
                    ]
                )
                Dashboard(content=maps.Geo(data=data))
                ```
        """
        super().__init__(
            data=data,
            series=series,
            region_column=region_column,
            widget_id=widget_id,
            title=title,
            legend_position=legend_position,
            color_axis=color_axis,
            styling=styling,
            region=region,
            tooltips=tooltips,
        )

    def _build_widget_input(self) -> Dict[str, Any]:
        """Method to build map widget."""
        return {
            "title": (
                build_templated_strings(items=self._title) if self._title else None
            ),
            "colorAxis": self._color_axis.build(),
            "legend": self._legend_position.build(),
            "series": self._build_series(),
            "region": self._region.value,
            "styling": self._styling.build(),
            "tooltip": self._build_tooltips(),
        }

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where
                the data is present.

        Raises:
            TooltipItemColumnNotFoundError: if column(s) of tooltip(s) were not found
            MapColumnDataNotFoundError: if column(s) supposed to contain data were not
                found.
        """
        self._validate_map_data(data=data)
        self._validate_series(data=data)
