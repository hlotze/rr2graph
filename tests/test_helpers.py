"""Unit tests for rr2graph.helpers."""

import argparse
import os

import numpy as np
import pandas as pd
import pytest

from rr2graph.helpers import (
    binwidth_2_bins,
    calculate_weekly_ticks,
    ensure_output_dirs,
    load_config,
    print_info,
    valid_month,
)


# ---------------------------------------------------------
# valid_month()
# ---------------------------------------------------------

def test_valid_month_ok():
    assert valid_month("1") == 1
    assert valid_month("6") == 6


def test_valid_month_non_numeric():
    with pytest.raises(argparse.ArgumentTypeError):
        valid_month("abc")


def test_valid_month_out_of_range_low():
    with pytest.raises(argparse.ArgumentTypeError):
        valid_month("0")


def test_valid_month_out_of_range_high():
    with pytest.raises(argparse.ArgumentTypeError):
        valid_month("7")


# ---------------------------------------------------------
# load_config()
# ---------------------------------------------------------

def test_load_config_none():
    assert load_config(None) == {}


def test_load_config_missing(tmp_path, capsys):
    """Return an empty config when the file is missing."""
    path = tmp_path / "missing.yaml"
    out = load_config(str(path))
    captured = capsys.readouterr()
    assert out == {}
    assert "not found" in captured.out


def test_load_config_valid(tmp_path):
    """Load a valid YAML configuration file."""
    cfgfile = tmp_path / "cfg.yaml"
    cfgfile.write_text("excel: test.xlsx\nnum_of_months: 3\n")
    out = load_config(str(cfgfile))
    assert out["excel"] == "test.xlsx"
    assert out["num_of_months"] == 3


# ---------------------------------------------------------
# ensure_output_dirs()
# ---------------------------------------------------------

def test_ensure_output_dirs(tmp_path):
    """Create all required rr2graph output directories."""
    base = tmp_path / "out"
    ensure_output_dirs(str(base))

    assert (base / "png").exists()
    assert (base / "pdf").exists()
    assert (base / "svg").exists()


# ---------------------------------------------------------
# binwidth_2_bins()
# ---------------------------------------------------------

def test_binwidth_2_bins_ok():
    data = np.array([10, 20, 30])
    bins = binwidth_2_bins(data, 10)
    assert np.array_equal(bins, np.array([10, 20, 30, 40]))


def test_binwidth_2_bins_invalid():
    """Reject invalid histogram bin widths."""
    with pytest.raises(ValueError):
        binwidth_2_bins(np.array([1, 2, 3]), 0)


# ---------------------------------------------------------
# calculate_weekly_ticks()
# ---------------------------------------------------------

def test_calculate_weekly_ticks_weekly():
    """Generate weekly Monday-based date ticks."""
    dates = pd.to_datetime(["2025-01-10", "2025-01-20"])
    ticks = calculate_weekly_ticks(dates)

    # First tick must be Monday.
    assert ticks[0].weekday() == 0

    # Last tick must be Monday.
    assert ticks[-1].weekday() == 0

    # Ensure weekly spacing.
    diffs = np.diff(ticks)
    assert all(d == np.timedelta64(7, "D") for d in diffs)


# ---------------------------------------------------------
# print_info()
# ---------------------------------------------------------

def test_print_info_runs(capsys):
    """Ensure print_info() generates CLI output."""
    print_info()
    captured = capsys.readouterr()
    assert "rr2graph info" in captured.out


def test_print_info_no_config(monkeypatch, capsys, tmp_path):
    """Handle missing config.yaml files gracefully."""
    # Switch working directory without a config.yaml file.
    monkeypatch.chdir(tmp_path)

    print_info()
    out = capsys.readouterr().out

    assert "No config file found" in out


def test_print_info_with_config(monkeypatch, capsys, tmp_path):
    """Display parsed configuration information."""
    # Create a temporary config.yaml file.
    cfg = tmp_path / "config.yaml"
    cfg.write_text("excel: test.xlsx\nnum_of_months: 3\noutput: out/")

    monkeypatch.chdir(tmp_path)

    print_info()
    out = capsys.readouterr().out

    assert "Detected config file" in out
    assert "Excel file" in out
    assert "Months" in out
    assert "Output directory" in out


def test_print_info_config_exception(monkeypatch, capsys, tmp_path):
    """Handle invalid configuration files gracefully."""
    from rr2graph.helpers import print_info

    # Switch into the temporary working directory.
    monkeypatch.chdir(tmp_path)

    # Create an invalid binary config.yaml file.
    cfg = tmp_path / "config.yaml"
    cfg.write_bytes(b"\x00\xFF\x00\xFFINVALID YAML\x00")

    print_info()
    out = capsys.readouterr().out

    assert "Warning: Failed to read config" in out
