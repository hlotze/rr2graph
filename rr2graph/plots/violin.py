"""
Violin plot visualization utilities for rr2graph.

This module contains violin-plot-based visualization components used
within the rr2graph monthly dashboard pipeline.

The provided violin visualizations support:
    - RR systolic value distributions
    - RR diastolic value distributions
    - heart rate distributions
    - compact statistical overview rendering

Violin plots are primarily used to visualize value density,
distribution shape and statistical spread characteristics.
"""

# Use a non-interactive backend for automated rendering environments.
import matplotlib

matplotlib.use("Agg")
import matplotlib.axes
import seaborn as sns

import pandas as pd


def generate_rr_violin_plot(
    df_heart: pd.DataFrame,
    violin_rr: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate RR systolic and diastolic violin plots.

    The visualization renders compact violin plots for RR systolic
    and RR diastolic measurement distributions.

    Visualization features:
        - statistical density visualization
        - embedded boxplot rendering
        - compact dashboard layout
        - normalized RR styling

    Args:
        df_heart:
            RR measurement dataframe.

        violin_rr:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured violin plot axes instance or ``None`` when
            dummy axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid plotting data is encountered.

    Examples:
        Generate RR violin plots:

            generate_rr_violin_plot(df_heart, ax)
    """
    if violin_rr is None:
        # Tests may provide dummy axes objects → skip rendering.
        return None

    # Enable y-axis labels for shared dashboard layouts.
    violin_rr.tick_params(axis="y", labelleft=True)
    # Render RR systolic distribution.
    sns.violinplot(
        df_heart["rr_syst"].to_list(),
        color="tab:blue",
        saturation=0.7,
        fill=False,
        inner="box",
        linewidth=0.8,
        ax=violin_rr,
    )
    # Render RR diastolic distribution.
    sns.violinplot(
        df_heart["rr_diast"].to_list(),
        color="tab:blue",
        saturation=0.7,
        fill=False,
        inner="box",
        linewidth=0.8,
        ax=violin_rr,
    )
    # Configure violin plot title.
    violin_rr.set_title("RR")
    return violin_rr


def generate_heart_rate_violin_plot(
    df_heart: pd.DataFrame,
    violin_hr: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate heart rate violin plots.

    The visualization renders compact violin plots for heart rate
    measurement distributions.

    Visualization features:
        - statistical density visualization
        - embedded boxplot rendering
        - compact dashboard layout
        - normalized medical styling

    Args:
        df_heart:
            RR measurement dataframe.

        violin_hr:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured violin plot axes instance or ``None`` when
            dummy axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid plotting data is encountered.

    Examples:
        Generate heart rate violin plots:

            generate_heart_rate_violin_plot(df_heart, ax)
    """
    if violin_hr is None:
        # Tests may provide dummy axes objects → skip rendering.
        return None

    # Enable y-axis labels for shared dashboard layouts.
    violin_hr.tick_params(axis="y", labelleft=True)
    # Render heart rate distribution.
    sns.violinplot(
        df_heart["heart_rate"].to_list(),
        color="tab:red",
        saturation=0.7,
        fill=False,
        inner="box",
        linewidth=0.8,
        ax=violin_hr,
    )
    # Configure violin plot title.
    violin_hr.set_title("Heart Rate")
    return violin_hr
