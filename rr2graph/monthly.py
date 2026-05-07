"""collection of the plot functions"""

# import numpy as np
import pandas as pd
import matplotlib.axes
from .plots.scatter import generate_scatter_plot
from .plots.hist import generate_rr_hist_plot, generate_heart_rate_hist_plot
from .plots.violin import generate_rr_violin_plot, generate_heart_rate_violin_plot
from .plots.box_swarm import (
    generate_rr_box_swarm_plot,
    generate_heart_rate_box_swarm_plot,
)


def gen_row_of_3_grapics_for_one_month_histo(
    month: pd.Period,
    axs: matplotlib.axes.Axes,
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """generate 3 axes in a row for on month's graphics
    i.e. scatter, histo, histo"""

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
    axs: matplotlib.axes.Axes,
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """generate 3 axes in a row for on month's graphics
    i.e. scatter, violin, violin"""

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
    axs: matplotlib.axes.Axes,
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
) -> None:
    """generate 3 axes in a row for on month's graphics
    i.e. scatter, box_swarm, box_swarm"""

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


def gen_req_plot_type(
    plot_type: str,
    num_of_months: int,
    df_heart: pd.DataFrame,
    df_weight: pd.DataFrame,
    axs,
) -> str:
    """orchestration for generation of
    the requested plot_types for
    for the num_of_months"""

    match plot_type:
        case "histogram":
            row_func = gen_row_of_3_grapics_for_one_month_histo
        case "violin":
            row_func = gen_row_of_3_grapics_for_one_month_violin
        case "box_swarm":
            row_func = gen_row_of_3_grapics_for_one_month_box_swarm
        case _:
            raise KeyError(f"Unknown plot_type: {plot_type}")

    # -----------------------------------------
    # es sollen nur die Daten der aktuellsten
    # num_of_months (1..6) genommen werden
    # -----------------------------------------
    # Daten filtern - df_heart
    end_date = df_heart["date_time"].max()
    start_date = end_date - pd.DateOffset(months=num_of_months)
    # Filter auf Daten anwenden
    df_heart = df_heart[
        (df_heart["date_time"] >= start_date) & (df_heart["date_time"] <= end_date)
    ]

    # Daten filtern - df_weight
    end_date = df_weight["date"].max()
    start_date = end_date - pd.DateOffset(months=num_of_months)
    df_weight = df_weight[
        (df_weight["date"] >= start_date) & (df_weight["date"] <= end_date)
    ][["date", "weight"]]

    # Monate im gefilterten Zeitraum extrahieren (ältester → neuester)
    # als pd.Period
    months = (df_heart["date_time"].dt.to_period("M").sort_values().unique())[
        -num_of_months:
    ]  # nur die letzten num_of_months nehmen

    # 1-Monats-Fall
    if len(months) == 1:
        month = months[0]
        row_func(month, axs, df_heart, df_weight)

        start_month = month.start_time
        fn = f"({start_month.strftime('%Y-%m')}) " f"per month data and {plot_type}"

    # Mehr-Monats-Fall
    else:
        for axs_pos, month in enumerate(months):
            row_func(month, axs[axs_pos], df_heart, df_weight)

        start_month = months[0].start_time
        end_month = months[-1].end_time

        fn = (
            f"({start_month.strftime('%Y-%m')}__"
            f"{end_month.strftime('%Y-%m')} {len(months)} months) "
            f"per month data and {plot_type}"
        )

    return fn
