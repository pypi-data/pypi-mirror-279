"""Spec to build different series supported by timeseries widget."""

from typing import Any
from typing import Dict
from typing import Union

from .y_axis import YAxis
from .y_axis_mirror import MirrorYAxis

YAxisSpec = Union[
    YAxis,
    MirrorYAxis,
]


def build_timeseries_y_axis(axis: YAxisSpec) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Args:
        axis (YAxisSpec): axis spec

    Returns:
        Input object for Dashboard API
    """
    return {**{_get_input_key(axis): axis.build()}}


def _get_input_key(axis: YAxisSpec) -> str:
    if isinstance(axis, YAxis):
        result = "standard"
    elif isinstance(axis, MirrorYAxis):
        result = "mirror"
    else:
        raise TypeError("Timeseries axis requires one of YAxis, MirrorYAxis instances.")

    return result
