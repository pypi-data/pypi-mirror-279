"""Main file that has a timeseries widget in a dashboard."""

import pandas as pd

from engineai.sdk.dashboard import dashboard
from engineai.sdk.dashboard.widgets import timeseries

timeseries_widget = timeseries.Timeseries(
    date_column="date",
    data=pd.read_json("data/example.json", orient="records"),
)

dashboard.Dashboard(
    slug="new_dashboard",
    content=[
        timeseries_widget,
    ],
)
