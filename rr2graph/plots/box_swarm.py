"""
Box/swarm plot visualization utilities for rr2graph.

This module contains combined boxplot and swarmplot visualization
components used within the rr2graph monthly dashboard pipeline.

The provided visualizations support:
    - RR systolic value distributions
    - RR diastolic value distributions
    - heart rate distributions
    - compact statistical outlier visualization

The box/swarm visualizations combine statistical summaries with raw
measurement point rendering to improve distribution transparency.
"""

# Use a non-interactive backend for automated rendering environments.
import matplotlib

matplotlib.use("Agg")
import matplotlib.axes
import seaborn as sns

import pandas as pd


def generate_rr_box_swarm_plot(
    df_heart: pd.DataFrame,
    box_swarm_rr: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate RR systolic and diastolic box/swarm plots.

    The visualization combines statistical boxplots with swarm-based
    raw measurement point rendering.

    Visualization features:
        - compact dashboard layout
        - statistical outlier visualization
        - raw measurement transparency
        - normalized RR styling

    Args:
        df_heart:
            RR measurement dataframe.

        box_swarm_rr:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured box/swarm axes instance or ``None`` when dummy
            axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid plotting data is encountered.

    Examples:
        Generate RR box/swarm plots:

            generate_rr_box_swarm_plot(df_heart, ax)
    """
    if box_swarm_rr is None:
        # Tests may provide dummy axes objects → skip rendering.
        return None

    # Enable y-axis labels for shared dashboard layouts.
    box_swarm_rr.tick_params(axis="y", labelleft=True)

    # Render RR systolic statistical boxplot.
    sns.boxplot(
        data=df_heart,
        y="rr_syst",
        color="tab:blue",
        saturation=0.7,
        fill=False,
        linewidth=0.8,
        ax=box_swarm_rr,
    )
    # Render RR diastolic statistical boxplot.
    sns.boxplot(
        data=df_heart,
        y="rr_diast",
        color="tab:blue",
        saturation=0.5,
        fill=False,
        linewidth=0.8,
        ax=box_swarm_rr,
    )
    # Render RR systolic raw measurement points.
    sns.swarmplot(
        data=df_heart,
        y="rr_syst",
        color="tab:blue",
        alpha=0.7,
        size=3,
        ax=box_swarm_rr,
    )
    # Render RR diastolic raw measurement points.
    sns.swarmplot(
        data=df_heart,
        y="rr_diast",
        color="tab:blue",
        alpha=0.5,
        size=3,
        ax=box_swarm_rr,
    )

    # Configure compact dashboard axis layout.
    box_swarm_rr.set_ylabel(None)
    box_swarm_rr.set_xticks([])
    box_swarm_rr.set_title("RR")

    return box_swarm_rr


def generate_heart_rate_box_swarm_plot(
    df_heart: pd.DataFrame,
    box_swarm_hr: matplotlib.axes.Axes,
) -> matplotlib.axes.Axes | None:
    """
    Generate heart rate box/swarm plots.

    The visualization combines statistical boxplots with swarm-based
    raw heart rate measurement rendering.

    Visualization features:
        - compact dashboard layout
        - statistical outlier visualization
        - raw measurement transparency
        - normalized medical styling

    Args:
        df_heart:
            RR measurement dataframe.

        box_swarm_hr:
            Target matplotlib axes instance.

    Returns:
        matplotlib.axes.Axes | None:
            Configured box/swarm axes instance or ``None`` when dummy
            axes are used during testing.

    Raises:
        KeyError:
            Raised when required dataframe columns are missing.

        ValueError:
            Raised when invalid plotting data is encountered.

    Examples:
        Generate heart rate box/swarm plots:

            generate_heart_rate_box_swarm_plot(df_heart, ax)
    """
    if box_swarm_hr is None:
        # Tests may provide dummy axes objects → skip rendering.
        return None

    # Enable y-axis labels for shared dashboard layouts.
    box_swarm_hr.tick_params(axis="y", labelleft=True)

    # Render heart rate statistical boxplot.
    sns.boxplot(
        data=df_heart,
        y="heart_rate",
        color="tab:red",
        saturation=0.7,
        fill=False,
        linewidth=0.8,
        ax=box_swarm_hr,
    )
    # Render raw heart rate measurement points.
    sns.swarmplot(
        data=df_heart,
        y="heart_rate",
        color="tab:red",
        alpha=0.7,
        size=3,
        ax=box_swarm_hr,
    )

    # Configure compact dashboard axis layout.
    box_swarm_hr.set_ylabel(None)
    box_swarm_hr.set_xticks([])
    box_swarm_hr.set_title("Heart Rate")

    return box_swarm_hr
