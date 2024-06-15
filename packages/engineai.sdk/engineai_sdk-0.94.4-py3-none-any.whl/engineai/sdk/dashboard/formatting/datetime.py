"""Formatting spec for dates."""

import enum
import warnings
from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.base import AbstractFactory


class DateTimeUnit(enum.Enum):
    """DateTime units."""

    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"


class DateTimeFormatting(AbstractFactory):
    """Date and time value formatting.

    Description for formatting date and time values,
    specifying template and time unit.
    """

    def __init__(
        self,
        *,
        template: Optional[str] = None,
        time_unit: DateTimeUnit = DateTimeUnit.DATE
    ):
        """Constructor for DateTimeFormatting.

        Args:
            template (Optional[str]): using spec from
                https://date-fns.org/v1.30.1/docs/format
            time_unit (DateTimeUnit): determines part of timestamp to consider.
                Defaults to DateTimeUnit.DATE.
        """
        super().__init__()
        if template:
            warnings.warn(
                "DateTimeFormatting `template` is deprecated, "
                "will be removed in next Major version.",
                DeprecationWarning,
            )
        default_template = {
            DateTimeUnit.DATE.value: "dd/MM/yyy",
            DateTimeUnit.TIME.value: "hh:mm",
            DateTimeUnit.DATETIME.value: "dd/MM/yyy hh:mm",
        }

        self.__template = (
            default_template[time_unit.value] if not template else template
        )
        self.__time_unit = time_unit

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "template": self.__template,
            "timeUnit": self.__time_unit.value,
        }
