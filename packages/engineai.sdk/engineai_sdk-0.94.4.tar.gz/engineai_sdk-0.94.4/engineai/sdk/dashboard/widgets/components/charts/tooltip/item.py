"""Spec to build tooltip items supported by different charts."""

from typing import Any
from typing import Dict

from ..typing import TooltipItem
from .category import CategoryTooltipItem
from .country import CountryTooltipItem
from .datetime import DatetimeTooltipItem
from .number import NumberTooltipItem
from .text import TextTooltipItem


def build_tooltip_item(item: TooltipItem) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Args:
        item (TooltipItem): item spec

    Returns:
        Input object for Dashboard API
    """
    return {**{_get_input_key(item): item.build()}}


def _get_input_key(item: TooltipItem) -> str:
    if isinstance(item, NumberTooltipItem):
        return "number"
    elif isinstance(item, TextTooltipItem):
        return "text"
    elif isinstance(item, DatetimeTooltipItem):
        return "dateTime"
    elif isinstance(item, CategoryTooltipItem):
        return "categorical"
    elif isinstance(item, CountryTooltipItem):
        return "country"
    else:
        raise TypeError(
            "item needs to be one of CategoryItem, DateTimeItem, "
            "NumberItem, TextItem"
        )
