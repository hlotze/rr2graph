"""collection of the plot functions"""

from __future__ import annotations
from typing import Callable, Sequence
from pathlib import Path

import pandas as pd

import matplotlib

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
    return {
        "png": subdirs["png"] / f"{filename}.png",
        "pdf": subdirs["pdf"] / f"{filename}.pdf",
        "svg": subdirs["svg"] / f"{filename}.svg",
    }


def _filter_last_months(
    df: pd.DataFrame, date_col: str, num_months: int
) -> pd.DataFrame:
    end_date = df[date_col].max()
    start_date = end_date - pd.DateOffset(months=num_months)
    return df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]


def _extract_months(df_heart: pd.DataFrame, num_months: int) -> list[pd.Period]:
    months = df_heart["date_time"].dt.to_period("M").sort_values().unique()
    return list(months[-num_months:])


# ---------------------------------------------------------
# Plot‑Row‑Funktionen
# ---------------------------------------------------------


def gen_row_of_3_grapics_for_one_month_histo(
    month: pd.Period,
    axs: Sequence[Axes],
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """Generates a row of 3 graphics for one month:
    scatter, rr histogram, heart rate histogram"""
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
    """Generates a row of 3 graphics for one month:
    scatter, rr violin, heart rate violin"""
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
    """Generates a row of 3 graphics for one month:
    scatter, rr box_swarm, heart rate box_swarm"""
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
# gen_req_plot_type
# ---------------------------------------------------------


def gen_req_plot_type(
    plot_type: str,
    num_of_months: int,
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
    axs: Axes | Sequence[Axes],
) -> str:
    """Generates the requested plot type for the given data and axes."""

    dispatch: dict[str, RowFunc] = {
        "histogram": gen_row_of_3_grapics_for_one_month_histo,
        "violin": gen_row_of_3_grapics_for_one_month_violin,
        "box_swarm": gen_row_of_3_grapics_for_one_month_box_swarm,
    }

    if plot_type not in dispatch:
        raise KeyError(f"Unknown plot_type: {plot_type}")

    row_func = dispatch[plot_type]

    df_heart = _filter_last_months(df_heart, "date_time", num_of_months)
    df_weight = _filter_last_months(df_weight, "date", num_of_months)[
        ["date", "weight"]
    ]

    months = _extract_months(df_heart, num_of_months)

    if len(months) == 1:
        month = months[0]
        row_func(month, axs, df_heart, df_weight)
        start_month = month.start_time
        return f"({start_month.strftime('%Y-%m')}) per month data and {plot_type}"

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
    """Generates the requested plot type for
    the last num_of_months months and
    saves them to the specified output directory."""
    fig, axs = get_needed_fig_and_axs_array(num_of_months)

    filename = gen_req_plot_type(
        plot_type=plot_type,
        num_of_months=num_of_months,
        df_heart=df_heart,
        df_weight=df_weight,
        axs=axs,
    )

    subdirs = _ensure_output_dirs(out_dir)
    paths = _build_output_paths(subdirs, filename)

    for fmt, path in paths.items():
        fig.savefig(path, format=fmt)

    plt.close(fig)

    return [str(p) for p in paths.values()]
