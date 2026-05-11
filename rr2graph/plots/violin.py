"""functions for the violin plots"""

import matplotlib.axes
import pandas as pd
import seaborn as sns


def generate_rr_violin_plot(
    df_heart: pd.DataFrame, violin_rr: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """violin plot for rr_sys and rr_diast"""
    if violin_rr is None:
        return None

    violin_rr.tick_params(axis="y", labelleft=True)
    sns.violinplot(
        df_heart["rr_syst"].to_list(),
        color="tab:blue",
        saturation=0.7,
        fill=False,
        inner="box",
        linewidth=0.8,
        ax=violin_rr,
    )
    sns.violinplot(
        df_heart["rr_diast"].to_list(),
        color="tab:blue",
        saturation=0.7,
        fill=False,
        inner="box",
        linewidth=0.8,
        ax=violin_rr,
    )
    violin_rr.set_title("RR")
    return violin_rr


def generate_heart_rate_violin_plot(
    df_heart: pd.DataFrame, violin_hr: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """violin plot for heart_rate"""
    if violin_hr is None:
        return None

    violin_hr.tick_params(axis="y", labelleft=True)
    sns.violinplot(
        df_heart["heart_rate"].to_list(),
        color="tab:red",
        saturation=0.7,
        fill=False,
        inner="box",
        linewidth=0.8,
        ax=violin_hr,
    )
    violin_hr.set_title("Heart Rate")
    return violin_hr
