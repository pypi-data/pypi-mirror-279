"""Spec for Widget Stacked Bar Chart Styling."""

from typing import Any
from typing import Dict

from ..base import BaseItemStyling


class StackedBarChartItemStyling(BaseItemStyling):
    """Spec for styling used by Stacked Bar Chart Item."""

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"showTotalOnTooltip": False}
