"""
Monthly visualization generation pipeline for rr2graph.

This module contains the high-level plotting workflow used to generate
monthly RR visualization dashboards.

Responsibilities include:
    - monthly dataframe filtering
    - visualization dispatching
    - export path generation
    - plot row composition
    - multi-format figure export

The module acts as the bridge between the low-level plotting modules
and the orchestration layer.
"""

from __future__ import annotations
from typing import Callable, Sequence
from pathlib import Path

import pandas as pd

import matplotlib

# Use a headless matplotlib backend for automated rendering.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from .layout import get_needed_fig_and_axs_array

from .plots.scatter import generate_scatter_plot
from .plots.hist import (
    generate_rr_hist_plot,
    generate_heart_rate_hist_plot,
)
from .plots.violin import (
    generate_rr_violin_plot,
    generate_heart_rate_violin_plot,
)
from .plots.box_swarm import (
    generate_rr_box_swarm_plot,
    generate_heart_rate_box_swarm_plot,
)

# ---------------------------------------------------------
# Private Helpers
# ---------------------------------------------------------


RowFunc = Callable[[pd.Period, Sequence[Axes], pd.DataFrame, pd.DataFrame], None]


def _ensure_output_dirs(base_dir: str | Path) -> dict[str, Path]:
    """
    Ensure export subdirectories exist.

    Creates normalized output directories for all supported export
    formats.

    Args:
        base_dir:
            Base export directory.

    Returns:
        dict[str, Path]:
            Mapping of export format names to output paths.
    """
    base = Path(base_dir)
    dirs = {
        "png": base / "png",
        "pdf": base / "pdf",
        "svg": base / "svg",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def _build_output_paths(subdirs: dict[str, Path], filename: str) -> dict[str, Path]:
    """
    Build normalized export file paths.

    Args:
        subdirs:
            Export directory mapping.

        filename:
            Base filename without extension.

    Returns:
        dict[str, Path]:
            Mapping of export formats to file paths.
    """
    return {
        "png": subdirs["png"] / f"{filename}.png",
        "pdf": subdirs["pdf"] / f"{filename}.pdf",
        "svg": subdirs["svg"] / f"{filename}.svg",
    }


def _filter_last_months(
    df: pd.DataFrame, date_col: str, num_months: int
) -> pd.DataFrame:
    """
    Filter a dataframe to the most recent months.

    Args:
        df:
            Source dataframe.

        date_col:
            Datetime column name.

        num_months:
            Number of months to retain.

    Returns:
        pd.DataFrame:
            Filtered dataframe.
    """
    end_date = df[date_col].max()
    start_date = end_date - pd.DateOffset(months=num_months)
    return df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]


def _extract_months(df_heart: pd.DataFrame, num_months: int) -> list[pd.Period]:
    """
    Extract normalized monthly periods from RR data.

    Args:
        df_heart:
            RR measurement dataframe.

        num_months:
            Maximum number of months to return.

    Returns:
        list[pd.Period]:
            Sorted list of monthly periods.
    """
    months = df_heart["date_time"].dt.to_period("M").sort_values().unique()
    return list(months[-num_months:])


# ---------------------------------------------------------
# Plot Row Generator Functions
# ---------------------------------------------------------


def gen_row_of_3_grapics_for_one_month_histo(
    month: pd.Period,
    axs: Sequence[Axes],
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """
    Generate a histogram-based monthly visualization row.

    The generated row contains:
        - RR scatter plot
        - RR histogram
        - heart rate histogram

    Args:
        month:
            Target month.

        axs:
            Row axis collection.

        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.
    """
    generate_scatter_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month],
        df_weight[df_weight["date"].dt.to_period("M") == month],
        axs[0],
    )
    generate_rr_hist_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month], 5, axs[1]
    )
    generate_heart_rate_hist_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month], 5, axs[2]
    )


def gen_row_of_3_grapics_for_one_month_violin(
    month: pd.Period,
    axs: Sequence[Axes],
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """
    Generate a violin-plot-based monthly visualization row.

    The generated row contains:
        - RR scatter plot
        - RR violin plot
        - heart rate violin plot

    Args:
        month:
            Target month.

        axs:
            Row axis collection.

        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.
    """
    generate_scatter_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month],
        df_weight[df_weight["date"].dt.to_period("M") == month],
        axs[0],
    )
    generate_rr_violin_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month], axs[1]
    )
    generate_heart_rate_violin_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month], axs[2]
    )


def gen_row_of_3_grapics_for_one_month_box_swarm(
    month: pd.Period,
    axs: Sequence[Axes],
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """
    Generate a box/swarm-based monthly visualization row.

    The generated row contains:
        - RR scatter plot
        - RR box/swarm plot
        - heart rate box/swarm plot

    Args:
        month:
            Target month.

        axs:
            Row axis collection.

        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.
    """
    generate_scatter_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month],
        df_weight[df_weight["date"].dt.to_period("M") == month],
        axs[0],
    )
    generate_rr_box_swarm_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month], axs[1]
    )
    generate_heart_rate_box_swarm_plot(
        df_heart[df_heart["date_time"].dt.to_period("M") == month], axs[2]
    )


# ---------------------------------------------------------
# Plot Type Dispatcher
# ---------------------------------------------------------


def gen_req_plot_type(
    plot_type: str,
    num_of_months: int,
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
    axs: Axes | Sequence[Axes],
) -> str:
    """
    Generate the requested monthly visualization strategy.

    The function dispatches the requested plot type to the appropriate
    monthly row generator implementation.

    Supported plot types:
        - histogram
        - violin
        - box_swarm

    Args:
        plot_type:
            Requested visualization type.

        num_of_months:
            Number of months to visualize.

        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.

        axs:
            Matplotlib axis container.

    Returns:
        str:
            Generated export filename.

    Raises:
        KeyError:
            Raised when an unsupported plot type is requested.
    """
    # Map plot identifiers to monthly row generator implementations.
    dispatch: dict[str, RowFunc] = {
        "histogram": gen_row_of_3_grapics_for_one_month_histo,
        "violin": gen_row_of_3_grapics_for_one_month_violin,
        "box_swarm": gen_row_of_3_grapics_for_one_month_box_swarm,
    }

    if plot_type not in dispatch:
        raise KeyError(f"Unknown plot_type: {plot_type}")

    row_func = dispatch[plot_type]

    # Restrict datasets to the configured monthly time window.
    df_heart = _filter_last_months(df_heart, "date_time", num_of_months)
    df_weight = _filter_last_months(df_weight, "date", num_of_months)[
        ["date", "weight"]
    ]

    # Extract all available monthly periods.
    months = _extract_months(df_heart, num_of_months)

    if len(months) == 1:
        month = months[0]
        row_func(month, axs, df_heart, df_weight)
        start_month = month.start_time
        return f"({start_month.strftime('%Y-%m')}) per month data and {plot_type}"

    # Generate one visualization row per month.
    for ax, month in zip(axs, months):
        row_func(month, ax, df_heart, df_weight)

    start_month = months[0].start_time
    end_month = months[-1].end_time

    return (
        f"({start_month.strftime('%Y-%m')}__"
        f"{end_month.strftime('%Y-%m')} {len(months)} months) "
        f"per month data and {plot_type}"
    )


# ---------------------------------------------------------
# generate_monthly_plots
# ---------------------------------------------------------


def generate_monthly_plots(
    plot_type: str,
    num_of_months: int,
    df_heart,
    df_weight,
    out_dir: str | Path,
) -> list[str]:
    """
    Generate and export monthly RR visualizations.

    This function represents the high-level monthly rendering pipeline
    used by the rr2graph orchestration layer.

    Workflow steps:
        1. Allocate figure and axes
        2. Generate requested visualization type
        3. Create export directories
        4. Export figures to all supported formats
        5. Release matplotlib resources

    Args:
        plot_type:
            Requested visualization type.

        num_of_months:
            Number of months to visualize.

        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.

        out_dir:
            Base export directory.

    Returns:
        list[str]:
            List of generated export file paths.

    Raises:
        RuntimeError:
            Raised when matplotlib rendering fails.

        OSError:
            Raised when export operations fail.
    """
    # Allocate figure and axes layout.
    fig, axs = get_needed_fig_and_axs_array(num_of_months)

    # Generate the requested visualization strategy.
    filename = gen_req_plot_type(
        plot_type=plot_type,
        num_of_months=num_of_months,
        df_heart=df_heart,
        df_weight=df_weight,
        axs=axs,
    )

    # Prepare export directory structure and file paths.
    subdirs = _ensure_output_dirs(out_dir)
    paths = _build_output_paths(subdirs, filename)

    # Export the rendered figure into all configured formats.
    for fmt, path in paths.items():
        fig.savefig(path, format=fmt)

    # Release matplotlib resources.
    plt.close(fig)

    return [str(p) for p in paths.values()]
