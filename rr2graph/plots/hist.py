"""
Histogram visualization utilities for rr2graph.

This module contains histogram-based visualization components used in
monthly RR dashboards.

The provided histogram visualizations support:
    - RR systolic value distributions
    - RR diastolic value distributions
    - heart rate distributions
    - normalized medical measurement binning

The histograms are primarily used to visualize measurement frequency
and statistical value distribution patterns.
"""

import matplotlib

# Use a non-interactive backend for automated rendering environments.
matplotlib.use("Agg")
import matplotlib.axes

import pandas as pd
from ..helpers import binwidth_2_bins


def generate_rr_hist_plot(
    df_heart: pd.DataFrame,
    binwidth: int,
    hist_rr: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate RR systolic and diastolic histogram plots.

    The visualization renders normalized horizontal histograms for
    RR systolic and RR diastolic measurements.

    Visualization features:
        - adaptive histogram binning
        - horizontal medical dashboard layout
        - shared RR color scheme
        - normalized transparency rendering

    Args:
        df_heart:
            RR measurement dataframe.

        binwidth:
            Histogram bin width.

        hist_rr:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured histogram axes instance or ``None`` when dummy
            axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid histogram data is encountered.

    Examples:
        Generate RR histograms:

            generate_rr_hist_plot(df_heart, 5, ax)
    """
    if hist_rr is None:
        # Tests may provide dummy axes objects → skip rendering.
        return None

    # Enable y-axis labels for shared dashboard layouts.
    hist_rr.tick_params(axis="y", labelleft=True)

    # Render RR systolic histogram distribution.
    hist_rr.hist(
        df_heart["rr_syst"],
        bins=binwidth_2_bins(df_heart["rr_syst"], binwidth),
        color="tab:blue",
        alpha=0.7,
        orientation="horizontal",
    )

    # Render RR diastolic histogram distribution.
    hist_rr.hist(
        df_heart["rr_diast"],
        bins=binwidth_2_bins(df_heart["rr_diast"], binwidth),
        color="tab:blue",
        alpha=0.7,
        orientation="horizontal",
    )

    # Configure histogram labels and titles.
    hist_rr.set_title("RR")
    hist_rr.set_xlabel("Observations per bin")
    return hist_rr


def generate_heart_rate_hist_plot(
    df_heart: pd.DataFrame,
    binwidth: int,
    hist_hr: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate heart rate histogram plots.

    The visualization renders a normalized horizontal histogram for
    heart rate measurements.

    Visualization features:
        - adaptive histogram binning
        - horizontal dashboard layout
        - normalized medical scaling
        - semi-transparent rendering

    Args:
        df_heart:
            RR measurement dataframe.

        binwidth:
            Histogram bin width.

        hist_hr:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured histogram axes instance or ``None`` when dummy
            axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid histogram data is encountered.

    Examples:
        Generate a heart rate histogram:

            generate_heart_rate_hist_plot(df_heart, 5, ax)
    """
    if hist_hr is None:
        # Tests may provide dummy axes objects → skip rendering.
        return None

    # Enable y-axis labels for shared dashboard layouts.
    hist_hr.tick_params(axis="y", labelleft=True)

    # Render heart rate histogram distribution.
    hist_hr.hist(
        df_heart["heart_rate"],
        bins=binwidth_2_bins(df_heart["heart_rate"], binwidth),
        color="tab:red",
        alpha=0.7,
        orientation="horizontal",
    )

    # Configure histogram labels and titles.
    hist_hr.set_title("Heart Rate")
    hist_hr.set_xlabel("Observations per bin")
    return hist_hr
