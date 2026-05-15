import os
import argparse
import numpy as np
import pandas as pd
import pytest

from rr2graph.helpers import (
    valid_month,
    load_config,
    ensure_output_dirs,
    binwidth_2_bins,
    calculate_weekly_ticks,
    print_info
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
    path = tmp_path / "missing.yaml"
    out = load_config(str(path))
    captured = capsys.readouterr()
    assert out == {}
    assert "nicht gefunden" in captured.out


def test_load_config_valid(tmp_path):
    cfgfile = tmp_path / "cfg.yaml"
    cfgfile.write_text("excel: test.xlsx\nnum_of_months: 3\n")
    out = load_config(str(cfgfile))
    assert out["excel"] == "test.xlsx"
    assert out["num_of_months"] == 3


# ---------------------------------------------------------
# ensure_output_dirs()
# ---------------------------------------------------------

def test_ensure_output_dirs(tmp_path):
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
    with pytest.raises(ValueError):
        binwidth_2_bins(np.array([1, 2, 3]), 0)


# ---------------------------------------------------------
# calculate_weekly_ticks()
# ---------------------------------------------------------

def test_calculate_weekly_ticks_weekly():
    dates = pd.to_datetime(["2025-01-10", "2025-01-20"])
    ticks = calculate_weekly_ticks(dates)

    # erster Tick = Montag
    assert ticks[0].weekday() == 0

    # letzter Tick = Montag
    assert ticks[-1].weekday() == 0

    # wöchentliche Frequenz
    diffs = np.diff(ticks)
    assert all(d == np.timedelta64(7, "D") for d in diffs)


# ---------------------------------------------------------
# print_info()
# ---------------------------------------------------------

def test_print_info_runs(capsys):
    print_info()
    captured = capsys.readouterr()
    assert "rr2graph info" in captured.out


def test_print_info_no_config(monkeypatch, capsys, tmp_path):
    # Arbeitsverzeichnis auf tmp_path setzen (ohne config.yaml)
    monkeypatch.chdir(tmp_path)

    print_info()
    out = capsys.readouterr().out

    assert "Keine Config-Datei gefunden" in out


def test_print_info_with_config(monkeypatch, capsys, tmp_path):
    # config.yaml erzeugen
    cfg = tmp_path / "config.yaml"
    cfg.write_text("excel: test.xlsx\nnum_of_months: 3\noutput: out/")

    monkeypatch.chdir(tmp_path)

    print_info()
    out = capsys.readouterr().out

    assert "Gefundene Config-Datei" in out
    assert "Excel-Datei" in out
    assert "Monate" in out
    assert "Output-Ordner" in out


def test_print_info_config_exception(monkeypatch, capsys, tmp_path):
    from rr2graph.helpers import print_info

    # Arbeitsverzeichnis wechseln
    monkeypatch.chdir(tmp_path)

    # config.yaml erzeugen, aber mit ungültigem (binärem) Inhalt
    cfg = tmp_path / "config.yaml"
    cfg.write_bytes(b"\x00\xFF\x00\xFFINVALID YAML\x00")

    print_info()
    out = capsys.readouterr().out

    assert "Warnung: Config konnte nicht gelesen werden" in out
