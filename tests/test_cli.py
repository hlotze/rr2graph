"""Unit tests for rr2graph.cli."""

import sys
from datetime import datetime

import pandas as pd

from rr2graph.cli import main, parse_args


# ---------------------------------------------------------
# parse_args() Tests
# ---------------------------------------------------------

def test_parse_args_basic():
    """Validate standard CLI argument parsing."""
    sys.argv = ["rr2graph", "-e", "data.xlsx", "-n", "3", "-o", "plots"]
    args = parse_args()

    assert args.excel == "data.xlsx"
    assert args.num_of_months == 3
    assert args.output == "plots"


def test_parse_args_info_flag():
    """Validate the --info CLI flag."""
    sys.argv = ["rr2graph", "--info"]
    args = parse_args()

    assert args.info is True


def test_parse_args_generate_test_data_flag():
    """Validate the --generate-test-data CLI flag."""
    sys.argv = ["rr2graph", "--generate-test-data"]
    args = parse_args()

    assert args.generate_test_data is True


# ---------------------------------------------------------
# main() Tests
# ---------------------------------------------------------

def test_main_calls_print_info(monkeypatch, capsys):
    """Ensure --info triggers print_info() and exits early."""
    sys.argv = ["rr2graph", "--info"]

    called = {"info": False}

    def fake_print_info():
        called["info"] = True

    monkeypatch.setattr("rr2graph.cli.print_info", fake_print_info)

    main()

    assert called["info"] is True


def test_main_calls_generate_test_data(monkeypatch, capsys):
    """Ensure --generate-test-data triggers test data generation."""
    sys.argv = ["rr2graph", "--generate-test-data"]

    called = {"gen": False}

    def fake_gen():
        called["gen"] = True

    monkeypatch.setattr("rr2graph.cli.generate_test_data_xlsx", fake_gen)

    main()

    assert called["gen"] is True


def test_main_runs_full_pipeline(monkeypatch, tmp_path, capsys):
    """Validate the normal CLI workflow using mocked dependencies."""
    sys.argv = [
        "rr2graph",
        "-e", "dummy.xlsx",
        "-n", "2",
        "-o", str(tmp_path / "plots")
    ]

    # Create temporary test dataframes.
    df_heart = pd.DataFrame({
        "date_time": [datetime(2025, 1, 1)],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
    })

    df_weight = pd.DataFrame({
        "date": [datetime(2025, 1, 1)],
        "weight": [80.0],
    })

    # Mock Excel reader functions.
    monkeypatch.setattr("rr2graph.cli.read_heart_data", lambda fn: df_heart)
    monkeypatch.setattr("rr2graph.cli.read_weight_data", lambda fn: df_weight)

    # Mock plot generation.
    def fake_generate_monthly_plots(plot_type, num, df_h, df_w, out):
        return [f"{plot_type}_dummy.png"]

    monkeypatch.setattr(
        "rr2graph.cli.generate_monthly_plots",
        fake_generate_monthly_plots
    )

    main()

    captured = capsys.readouterr()

    # Validate CLI console output.
    assert "Heart rows read: 1" in captured.out
    assert "Weight rows read: 1" in captured.out
    assert "Generating histogram plots…" in captured.out
    assert "Generating violin plots…" in captured.out
    assert "Generating box_swarm plots…" in captured.out
    assert "dummy.png" in captured.out
