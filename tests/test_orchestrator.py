"""Unit tests for rr2graph.orchestrator."""

from datetime import datetime

import pandas as pd
import pytest

from rr2graph.orchestrator import generate_monthly_plots


class DummyFig:
    """Minimal matplotlib figure replacement for savefig testing."""
    def __init__(self):
        self.saved_files = []

    def savefig(self, fn):
        self.saved_files.append(fn)

    def close(self):
        pass


def test_generate_monthly_plots_creates_three_files(tmp_path, monkeypatch):
    """Generate PNG, PDF, and SVG output files."""

    # Return a fake matplotlib figure.
    dummy_fig = DummyFig()

    def fake_get_fig_and_axs_array(num):
        axs = [[None, None, None] for _ in range(num)]
        return dummy_fig, axs

    def fake_gen_req_plot_type(plot_type, num, df_h, df_w, axs):
        return "(2025-01__2025-03 3 months) per month data and histogram"

    # Mock plotting helpers.
    monkeypatch.setattr(
        "rr2graph.orchestrator.get_needed_fig_and_axs_array",
        fake_get_fig_and_axs_array,
    )
    monkeypatch.setattr(
        "rr2graph.orchestrator.gen_req_plot_type",
        fake_gen_req_plot_type,
    )

    # Create temporary test datasets.
    df_heart = pd.DataFrame({
        "date_time": [
            datetime(2025, 1, 1),
            datetime(2025, 2, 1),
            datetime(2025, 3, 1),
        ],
        "rr_syst": [120, 125, 130],
        "rr_diast": [80, 82, 85],
        "heart_rate": [70, 72, 75],
    })

    df_weight = pd.DataFrame({
        "date": [
            datetime(2025, 1, 1),
            datetime(2025, 2, 1),
            datetime(2025, 3, 1),
        ],
        "weight": [80.0, 79.5, 79.0],
    })

    out_dir = tmp_path / "plots"

    files = generate_monthly_plots(
        "histogram",
        3,
        df_heart,
        df_weight,
        str(out_dir),
    )

    # Three output files must be generated.
    assert len(files) == 3

    # All expected file extensions must exist.
    assert any(f.endswith(".png") for f in files)
    assert any(f.endswith(".pdf") for f in files)
    assert any(f.endswith(".svg") for f in files)

    # Output directories must be created.
    assert (out_dir / "png").exists()
    assert (out_dir / "pdf").exists()
    assert (out_dir / "svg").exists()

    # savefig() must be called for each output format.
    assert len(dummy_fig.saved_files) == 3


def test_generate_monthly_plots_invalid_months():
    """Reject unsupported month counts."""
    df = pd.DataFrame({
        "date_time": [datetime(2025, 1, 1)],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
    })
    df_w = pd.DataFrame({
        "date": [datetime(2025, 1, 1)],
        "weight": [80.0],
    })

    with pytest.raises(SystemExit):
        generate_monthly_plots("histogram", 0, df, df_w, "plots")

    with pytest.raises(SystemExit):
        generate_monthly_plots("histogram", 7, df, df_w, "plots")


def test_generate_monthly_plots_closes_real_figure(tmp_path):
    """Ensure real matplotlib figures are closed correctly."""
    # Create minimal valid dataframes.
    df_heart = pd.DataFrame({
        "date_time": pd.to_datetime(["2024-01-01 10:00:00"]),
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
        "week": [1],
    })

    df_weight = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01"]),
        "weight": [80.0],
        "week": [1],
    })

    out = tmp_path

    # Use the real matplotlib figure implementation.
    files = generate_monthly_plots("histogram", 1, df_heart, df_weight, out)

    # Output files must be generated successfully.
    assert len(files) == 3
    for f in files:
        assert f.endswith((".png", ".pdf", ".svg"))
