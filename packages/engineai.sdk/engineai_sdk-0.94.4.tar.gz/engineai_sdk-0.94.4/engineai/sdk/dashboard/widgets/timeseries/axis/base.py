"""Specs for a Base Timeseries chart."""

from typing import Any
from typing import Dict
from typing import Mapping

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler


class TimeseriesBaseAxis(AbstractFactoryLinkItemsHandler):
    """Specs for a Base Timeseries chart."""

    @type_check
    def __init__(
        self,
        *,
        enable_crosshair: bool = False,
    ) -> None:
        """Construct TimeseriesBaseAxis.

        Args:
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
        """
        super().__init__()
        self.__enable_crosshair = enable_crosshair

    def _build_axis(self) -> Mapping[str, Any]:
        """Method that generates the input for a specific axis."""
        return {}

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API.
        """
        return {
            **self._build_axis(),
            "enableCrosshair": self.__enable_crosshair,
            "bands": [],
            "lines": [],
        }
