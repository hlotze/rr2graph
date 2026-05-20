"""
Scatter plot generation utilities for rr2graph.

This module contains the combined RR visualization scatter plot used
throughout the rr2graph monthly dashboard pipeline.

The generated visualization combines:
    - heart rate measurements
    - RR systolic/diastolic ranges
    - body weight measurements
    - weekly time axis normalization

The scatter visualization acts as the primary longitudinal overview
plot for monthly RR analysis.
"""

import matplotlib

# Use a non-interactive backend for automated rendering environments.
matplotlib.use("Agg")
import matplotlib.axes
from matplotlib.ticker import AutoMinorLocator

import pandas as pd

from ..helpers import calculate_weekly_ticks


def generate_scatter_plot(
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
    scatter: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate a combined RR scatter visualization.

    The visualization combines multiple longitudinal health metrics
    into a single monthly overview dashboard.

    Included metrics:
        - heart rate scatter points
        - RR systolic/diastolic ranges
        - body weight measurements

    Visualization features:
        - weekly tick normalization
        - major/minor grid rendering
        - adaptive month titles
        - shared medical unit scaling

    Args:
        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.

        scatter:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured scatter axes instance or ``None`` when dummy
            axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid plotting data is encountered.

    Examples:
        Generate a combined RR scatter plot:

            generate_scatter_plot(df_heart, df_weight, ax)
    """
    # Tests may provide dummy axes objects → skip rendering.
    if scatter is None:
        return None

    # Generate adaptive dashboard title.
    # Determine the displayed month range.
    start_month = df_heart["date_time"].min().to_period("M").start_time
    end_month = df_heart["date_time"].max().to_period("M").end_time

    if start_month.month == end_month.month and start_month.year == end_month.year:
        title = f"{start_month.strftime('%Y %B')}"
    else:
        title = f"{start_month.strftime('%Y %B')} - " f"{end_month.strftime('%Y %B')}"

    # Render heart rate scatter points.
    scatter.scatter(
        df_heart["date_time"],
        df_heart["heart_rate"],
        color="tab:red",
        label="Heart Rate",
    )

    # Render RR systolic/diastolic value ranges.
    scatter.vlines(
        df_heart["date_time"],
        df_heart["rr_diast"],
        df_heart["rr_syst"],
        colors="tab:blue",
        alpha=0.7,
        linewidth=1.5,
        label="RR",
    )

    # Render body weight measurement points.
    scatter.scatter(
        df_weight["date"], df_weight["weight"], color="green", label="Weight"
    )

    scatter.set_title(title)
    scatter.set_ylabel("RR (mm Hg)\nHeart Rate (bpm)\nWeight (kg)")

    # Generate normalized weekly tick labels.
    ticks = calculate_weekly_ticks(df_heart["date_time"])

    labels = [
        tick.strftime("%a %d.%m.") if tick.weekday() == 0 else "" for tick in ticks
    ]

    # Configure major and minor x-axis tick rendering.
    scatter.xaxis.set_minor_locator(AutoMinorLocator(7))
    scatter.set_xticks(ticks)
    scatter.set_xticklabels(labels)

    # Configure shared medical measurement scaling.
    scatter.set_yticks(range(50, 160, 10))
    scatter.set_yticklabels(range(50, 160, 10))

    # Configure grid rendering.
    scatter.grid(which="major")
    scatter.grid(which="minor", linestyle=":")

    scatter.legend(loc="upper left")

    return scatter
