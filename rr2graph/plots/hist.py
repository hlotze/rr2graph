"""functions for histo plots"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.axes

import pandas as pd
from ..helpers import binwidth_2_bins


def generate_rr_hist_plot(
    df_heart: pd.DataFrame, binwidth: int, hist_rr: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """histo plot for rr_syst and rr_diast data"""
    if hist_rr is None:
        return None

    hist_rr.tick_params(axis="y", labelleft=True)
    hist_rr.hist(
        df_heart["rr_syst"],
        bins=binwidth_2_bins(df_heart["rr_syst"], binwidth),
        color="tab:blue",
        alpha=0.7,
        orientation="horizontal",
    )
    hist_rr.hist(
        df_heart["rr_diast"],
        bins=binwidth_2_bins(df_heart["rr_diast"], binwidth),
        color="tab:blue",
        alpha=0.7,
        orientation="horizontal",
    )
    hist_rr.set_title("RR")
    hist_rr.set_xlabel("Observations per bin")
    return hist_rr


def generate_heart_rate_hist_plot(
    df_heart: pd.DataFrame, binwidth: int, hist_hr: matplotlib.axes.Axes
) -> matplotlib.axes.Axes:
    """histo plot for heart_rate data"""
    if hist_hr is None:
        return None

    hist_hr.tick_params(axis="y", labelleft=True)
    hist_hr.hist(
        df_heart["heart_rate"],
        bins=binwidth_2_bins(df_heart["heart_rate"], binwidth),
        color="tab:red",
        alpha=0.7,
        orientation="horizontal",
    )
    hist_hr.set_title("Heart Rate")
    hist_hr.set_xlabel("Observations per bin")
    return hist_hr
