"""funtions for box_swarm plots"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.axes
import seaborn as sns

import pandas as pd


def generate_rr_box_swarm_plot(
    df_heart: pd.DataFrame, box_swarm_rr: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """box_swarm plots for rr_sys and rr_diast data"""
    if box_swarm_rr is None:
        return None

    box_swarm_rr.tick_params(axis="y", labelleft=True)

    sns.boxplot(
        data=df_heart,
        y="rr_syst",
        color="tab:blue",
        saturation=0.7,
        fill=False,
        linewidth=0.8,
        ax=box_swarm_rr,
    )
    sns.boxplot(
        data=df_heart,
        y="rr_diast",
        color="tab:blue",
        saturation=0.5,
        fill=False,
        linewidth=0.8,
        ax=box_swarm_rr,
    )
    sns.swarmplot(
        data=df_heart,
        y="rr_syst",
        color="tab:blue",
        alpha=0.7,
        size=3,
        ax=box_swarm_rr,
    )
    sns.swarmplot(
        data=df_heart,
        y="rr_diast",
        color="tab:blue",
        alpha=0.5,
        size=3,
        ax=box_swarm_rr,
    )

    box_swarm_rr.set_ylabel(None)
    box_swarm_rr.set_xticks([])
    box_swarm_rr.set_title("RR")

    return box_swarm_rr


def generate_heart_rate_box_swarm_plot(
    df_heart: pd.DataFrame, box_swarm_hr: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """box_swarm plot for heart_rate data"""
    if box_swarm_hr is None:
        return None

    box_swarm_hr.tick_params(axis="y", labelleft=True)

    sns.boxplot(
        data=df_heart,
        y="heart_rate",
        color="tab:red",
        saturation=0.7,
        fill=False,
        linewidth=0.8,
        ax=box_swarm_hr,
    )
    sns.swarmplot(
        data=df_heart,
        y="heart_rate",
        color="tab:red",
        alpha=0.7,
        size=3,
        ax=box_swarm_hr,
    )

    box_swarm_hr.set_ylabel(None)
    box_swarm_hr.set_xticks([])
    box_swarm_hr.set_title("Heart Rate")

    return box_swarm_hr
