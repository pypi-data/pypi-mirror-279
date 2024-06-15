"""Spec for legend of a Map Shape widget."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.widgets.maps.enums import LegendPosition


class Legend(AbstractFactory):
    """Spec for legend of a Map widget."""

    @type_check
    def __init__(self, *, position: LegendPosition = LegendPosition.BOTTOM):
        """Constructor for Legend.

        Args:
            position (Position): location of position
                relative to data, maps.
        """
        super().__init__()
        self.__position = position

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {"position": self.__position.value}
