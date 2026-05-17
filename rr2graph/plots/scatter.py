"""functions for the scatter plot"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.axes
from matplotlib.ticker import AutoMinorLocator

import pandas as pd

from ..helpers import calculate_weekly_ticks


def generate_scatter_plot(
    df_heart: pd.DataFrame, df_weight: pd.DataFrame, scatter: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """
    Kombinierter Scatter-Plot:
    - Heart Rate Punkte
    - Weight Punkte
    - RR-Linien (vlines + plot-lines)
    """
    # Tests übergeben Dummy-Achsen → nicht plotten
    if scatter is None:
        return None

    # Titel bestimmen
    start_month = df_heart["date_time"].min().to_period("M").start_time
    end_month = df_heart["date_time"].max().to_period("M").end_time

    if start_month.month == end_month.month and start_month.year == end_month.year:
        title = f"{start_month.strftime('%Y %B')}"
    else:
        title = f"{start_month.strftime('%Y %B')} - " f"{end_month.strftime('%Y %B')}"

    # Heart Rate Punkte
    scatter.scatter(
        df_heart["date_time"],
        df_heart["heart_rate"],
        color="tab:red",
        label="Heart Rate",
    )

    # RR vlines (für echten Plot)
    scatter.vlines(
        df_heart["date_time"],
        df_heart["rr_diast"],
        df_heart["rr_syst"],
        colors="tab:blue",
        alpha=0.7,
        linewidth=1.5,
        label="RR",
    )

    # Weight Punkte
    scatter.scatter(
        df_weight["date"], df_weight["weight"], color="green", label="Weight"
    )

    scatter.set_title(title)
    scatter.set_ylabel("RR (mm Hg)\nHeart Rate (bpm)\nWeight (kg)")

    # x ticks and labels
    ticks = calculate_weekly_ticks(df_heart["date_time"])

    labels = [
        tick.strftime("%a %d.%m.") if tick.weekday() == 0 else "" for tick in ticks
    ]

    scatter.xaxis.set_minor_locator(AutoMinorLocator(7))
    scatter.set_xticks(ticks)
    scatter.set_xticklabels(labels)

    scatter.set_yticks(range(50, 160, 10))
    scatter.set_yticklabels(range(50, 160, 10))

    scatter.grid(which="major")
    scatter.grid(which="minor", linestyle=":")

    scatter.legend(loc="upper left")
    scatter.legend()

    return scatter
