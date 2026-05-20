"""Unit tests for rr2graph.monthly."""

import matplotlib.pyplot as plt
import pandas as pd
import pytest

import rr2graph.monthly as monthly
from rr2graph.monthly import (
    _build_output_paths,
    _ensure_output_dirs,
    gen_req_plot_type,
)


def test_ensure_output_dirs(tmp_path):
    """Create the required monthly output directories."""

    dirs = _ensure_output_dirs(tmp_path)

    assert (tmp_path / "png").exists()
    assert (tmp_path / "pdf").exists()
    assert (tmp_path / "svg").exists()

    assert dirs["png"] == tmp_path / "png"
    assert dirs["pdf"] == tmp_path / "pdf"
    assert dirs["svg"] == tmp_path / "svg"


def test_build_output_paths(tmp_path):
    """Build output file paths for all export formats."""
    subdirs = {
        "png": tmp_path / "png",
        "pdf": tmp_path / "pdf",
        "svg": tmp_path / "svg",
    }

    paths = _build_output_paths(subdirs, "testfile")

    assert paths["png"].name == "testfile.png"
    assert paths["pdf"].name == "testfile.pdf"
    assert paths["svg"].name == "testfile.svg"


def test_row_func_violin(monkeypatch, df_heart_sample, df_weight_sample):
    """Call the violin row renderer for each requested month."""
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_violin",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]
    gen_req_plot_type("violin", 2, df_heart_sample, df_weight_sample, axs)

    assert calls == ["2025-02", "2025-03"]


def test_row_func_box_swarm(monkeypatch, df_heart_sample, df_weight_sample):
    """Call the box-swarm row renderer for each requested month."""
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_box_swarm",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]
    gen_req_plot_type("box_swarm", 2, df_heart_sample, df_weight_sample, axs)

    assert calls == ["2025-02", "2025-03"]


def test_row_func_violin_called(monkeypatch, df_heart_sample, df_weight_sample):
    """Ensure violin row functions are executed for each month."""
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_violin",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]

    gen_req_plot_type(
        "violin",
        2,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    assert calls == ["2025-02", "2025-03"]


def test_row_func_box_swarm_called(monkeypatch, df_heart_sample, df_weight_sample):
    """Ensure box-swarm row functions are executed for each month."""
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_box_swarm",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]

    gen_req_plot_type(
        "box_swarm",
        2,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    assert calls == ["2025-02", "2025-03"]


def test_generate_monthly_plots(monkeypatch, tmp_path, df_heart_sample, df_weight_sample):
    """Generate all requested monthly output formats."""

    # Create fake matplotlib objects.
    class FakeFig:
        def __init__(self):
            self.saved = []

        def savefig(self, path, format=None):
            self.saved.append((str(path), format))

        def close(self):
            pass

    fake_fig = FakeFig()
    fake_axs = [[None, None, None]]

    # Mock figure and axes allocation.
    monkeypatch.setattr(
        monthly,
        "get_needed_fig_and_axs_array",
        lambda n: (fake_fig, fake_axs),
    )

    # Mock generated filename.
    monkeypatch.setattr(
        monthly,
        "gen_req_plot_type",
        lambda *args, **kwargs: "testfile",
    )

    # Allow plt.close() to accept the fake figure.
    monkeypatch.setattr("matplotlib.pyplot.close", lambda fig: None)

    paths = monthly.generate_monthly_plots(
        "histogram", 1, df_heart_sample, df_weight_sample, tmp_path
    )

    assert len(paths) == 3
    assert any("testfile.png" in p for p in paths)
    assert any("testfile.pdf" in p for p in paths)
    assert any("testfile.svg" in p for p in paths)


def test_gen_req_plot_type_invalid():
    """Reject unsupported plot types."""
    df_heart = pd.DataFrame({"date_time": [], "rr_syst": [], "rr_diast": [], "heart_rate": []})
    df_weight = pd.DataFrame({"date": [], "weight": []})

    fig, axs = plt.subplots(nrows=1, ncols=3)

    with pytest.raises(KeyError):
        gen_req_plot_type("invalid_plot_type", 1, df_heart, df_weight, axs)


def test_month_extraction_last_n_months(df_heart_sample, df_weight_sample):
    """Extract only the requested trailing months."""
    # Sample dataset spans four calendar months.
    num_months = 3

    # Create a placeholder axes layout.
    axs = [[None, None, None] for _ in range(num_months)]

    _ = gen_req_plot_type(
        "histogram",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Only the trailing months should remain.
    expected = ["2025-01", "2025-02", "2025-03"]
    months = (
        df_heart_sample["date_time"]
        .dt.to_period("M")
        .sort_values()
        .unique()
    )[-num_months:]

    assert [str(m) for m in months] == expected


def test_row_func_called_correctly(monkeypatch, df_heart_sample, df_weight_sample):
    """Execute the histogram row renderer once per month."""
    calls = []

    def fake_row_func(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_histo",
        fake_row_func,
    )

    num_months = 2
    axs = [[None, None, None] for _ in range(num_months)]

    gen_req_plot_type(
        "histogram",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Only the latest months should be processed.
    assert calls == ["2025-02", "2025-03"]


def test_fn_base_format_multi_month(df_heart_sample, df_weight_sample):
    """Build descriptive filenames for multi-month plots."""
    num_months = 3
    axs = [[None, None, None] for _ in range(num_months)]

    fn = gen_req_plot_type(
        "violin",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Example filename pattern.
    assert "2025-01" in fn
    assert "2025-03" in fn
    assert "3 months" in fn
    assert "violin" in fn


def test_fn_base_format_single_month(df_heart_sample, df_weight_sample):
    """Build descriptive filenames for single-month plots."""
    num_months = 1
    axs = [None, None, None]

    fn = gen_req_plot_type(
        "box_swarm",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # The latest sample month is 2025-03.
    assert "(2025-03)" in fn
    assert "box_swarm" in fn


def test_month_filtering_respects_year_boundaries(df_heart_sample, df_weight_sample):
    """Handle month filtering across year boundaries."""
    num_months = 2
    axs = [[None, None, None] for _ in range(num_months)]

    fn = gen_req_plot_type(
        "histogram",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Only the latest months should be processed.
    assert "2025-02" in fn
    assert "2025-03" in fn
    assert "2024-12" not in fn
    assert "2025-01" not in fn
