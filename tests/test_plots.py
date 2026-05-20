"""Unit tests for rr2graph plotting modules."""

from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pytest

matplotlib.use("Agg")  # Use a non-GUI backend for tests.

from rr2graph.plots.box_swarm import (
    generate_heart_rate_box_swarm_plot,
    generate_rr_box_swarm_plot,
)
from rr2graph.plots.hist import (
    generate_heart_rate_hist_plot,
    generate_rr_hist_plot,
)
from rr2graph.plots.scatter import generate_scatter_plot
from rr2graph.plots.violin import (
    generate_heart_rate_violin_plot,
    generate_rr_violin_plot,
)


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def df_heart_small():
    return pd.DataFrame(
        {
            "date_time": [
                datetime(2025, 1, 1, 8, 0),
                datetime(2025, 1, 2, 9, 0),
                datetime(2025, 1, 3, 10, 0),
            ],
            "rr_syst": [120, 125, 130],
            "rr_diast": [80, 82, 85],
            "heart_rate": [70, 72, 75],
        }
    )


@pytest.fixture
def df_weight_small():
    return pd.DataFrame(
        {
            "date": [
                datetime(2025, 1, 1, 10, 0),
                datetime(2025, 1, 2, 10, 0),
                datetime(2025, 1, 3, 10, 0),
            ],
            "weight": [80.0, 79.5, 79.0],
        }
    )


# ---------------------------------------------------------
# Scatter Plot
# ---------------------------------------------------------


def test_scatter_plot_runs(df_heart_small, df_weight_small):
    """Generate a scatter plot with RR and weight overlays."""
    _, ax = plt.subplots()
    out = generate_scatter_plot(df_heart_small, df_weight_small, ax)

    assert out is ax
    assert out.get_title() != ""
    assert len(out.collections) >= 2  # Heart-rate and weight overlays.
    # RR lines are stored as LineCollection objects.
    assert any(isinstance(c, matplotlib.collections.LineCollection) for c in out.collections)


# ---------------------------------------------------------
# Histograms
# ---------------------------------------------------------


def test_rr_hist_plot_runs(df_heart_small):
    """Generate an RR histogram plot."""
    _, ax = plt.subplots()
    out = generate_rr_hist_plot(df_heart_small, 5, ax)

    assert out is ax
    assert out.get_title() == "RR"
    assert out.get_xlabel() == "Observations per bin"
    assert len(out.patches) > 0  # Histogram bars must exist.


def test_hr_hist_plot_runs(df_heart_small):
    """Generate a heart-rate histogram plot."""
    _, ax = plt.subplots()
    out = generate_heart_rate_hist_plot(df_heart_small, 5, ax)

    assert out is ax
    assert out.get_title() == "Heart Rate"
    assert out.get_xlabel() == "Observations per bin"
    assert len(out.patches) > 0


# ---------------------------------------------------------
# Violin plots
# ---------------------------------------------------------


def test_rr_violin_plot_runs(df_heart_small):
    """Generate an RR violin plot."""
    _, ax = plt.subplots()
    out = generate_rr_violin_plot(df_heart_small, ax)

    assert out is ax
    assert out.get_title() == "RR"
    assert len(out.collections) > 0  # Violin artists must exist.


def test_hr_violin_plot_runs(df_heart_small):
    """Generate a heart-rate violin plot."""
    _, ax = plt.subplots()
    out = generate_heart_rate_violin_plot(df_heart_small, ax)

    assert out is ax
    assert out.get_title() == "Heart Rate"
    assert len(out.collections) > 0


# ---------------------------------------------------------
# Box-swarm plots
# ---------------------------------------------------------


def test_rr_box_swarm_plot_runs(df_heart_small):
    """Generate an RR box-swarm plot."""
    _, ax = plt.subplots()
    out = generate_rr_box_swarm_plot(df_heart_small, ax)

    assert out is ax
    assert out.get_title() == "RR"
    assert len(out.collections) > 0  # Swarm points must exist.
    assert len(out.artists) >= 0  # Box artists may exist.


def test_hr_box_swarm_plot_runs(df_heart_small):
    """Generate a heart-rate box-swarm plot."""
    _, ax = plt.subplots()
    out = generate_heart_rate_box_swarm_plot(df_heart_small, ax)

    assert out is ax
    assert out.get_title() == "Heart Rate"
    assert len(out.collections) > 0
