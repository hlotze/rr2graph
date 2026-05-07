import pandas as pd
import numpy as np
import pytest
from datetime import datetime

from rr2graph.io import (
    parse_excel_date,
    read_heart_data,
    read_weight_data,
)
from rr2graph.helpers import ensure_output_dirs


# ---------------------------------------------------------
# Hilfsfunktion zum Schreiben einer Excel-Datei
# ---------------------------------------------------------

def write_excel(tmp_path, df):
    fn = tmp_path / "test.xlsx"
    df.to_excel(fn, sheet_name="data", index=False)
    return fn


# ---------------------------------------------------------
# parse_excel_date()
# ---------------------------------------------------------

def test_parse_excel_date_dd_mm_yy():
    assert parse_excel_date("03.11.25") == pd.Timestamp(2025, 11, 3)


def test_parse_excel_date_dd_mm_yyyy():
    assert parse_excel_date("03.11.2025") == pd.Timestamp(2025, 11, 3)


def test_parse_excel_date_iso():
    assert parse_excel_date("2025-11-03") == pd.Timestamp(year=2025, month=3, day=11)


def test_parse_excel_date_excel_int():
    # Excel-Seriendatum 45231 entspricht in Pandas 2023-11-01
    assert parse_excel_date(45231) == pd.Timestamp(year=2023, month=11, day=1)


def test_parse_excel_date_excel_float():
    # Excel-Seriendatum 45231 entspricht in Pandas 2023-11-01
    assert parse_excel_date(45231) == pd.Timestamp(year=2023, month=11, day=1)


def test_parse_excel_date_excel_str():
    assert parse_excel_date("45231") == pd.Timestamp("2023-11-01")


def test_parse_excel_date_timestamp_passthrough():
    ts = pd.Timestamp("2025-11-03")
    assert parse_excel_date(ts) == ts


def test_parse_excel_date_invalid():
    assert pd.isna(parse_excel_date("not-a-date"))


# ---------------------------------------------------------
# read_heart_data()
# ---------------------------------------------------------

def test_read_heart_data_parses_dd_mm_yy(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25"],
        "time": ["08:30:00"],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
        "weight": [80.0],
    })

    fn = write_excel(tmp_path, df)
    out = read_heart_data(fn)

    assert len(out) == 1
    assert out["date_time"].iloc[0] == datetime(2025, 11, 3, 8, 30)
    assert out["week"].iloc[0] == datetime(2025, 11, 3).isocalendar().week


def test_read_heart_data_drops_missing_time(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25"],
        "time": [""],  # ungültig
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
        "weight": [80.0],
    })

    fn = write_excel(tmp_path, df)
    out = read_heart_data(fn)

    assert len(out) == 0


def test_read_heart_data_multiple_rows(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25", "04.11.25"],
        "time": ["08:00:00", "09:00:00"],
        "rr_syst": [120, 130],
        "rr_diast": [80, 85],
        "heart_rate": [70, 75],
        "weight": [80.0, 79.5],
    })

    fn = write_excel(tmp_path, df)
    out = read_heart_data(fn)

    assert len(out) == 2
    assert list(out["rr_syst"]) == [120, 130]


# ---------------------------------------------------------
# read_weight_data()
# ---------------------------------------------------------

def test_read_weight_data_parses_dd_mm_yy(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25"],
        "weight": [80.0],
        "time": ["08:00:00"],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
    })

    fn = write_excel(tmp_path, df)
    out = read_weight_data(fn)

    assert len(out) == 1
    assert out["date"].iloc[0] == datetime(2025, 11, 3, 10, 0)
    assert out["week"].iloc[0] == datetime(2025, 11, 3).isocalendar().week


def test_read_weight_data_invalid_weight(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25"],
        "weight": ["not-a-number"],
        "time": ["08:00:00"],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
    })

    fn = write_excel(tmp_path, df)
    out = read_weight_data(fn)

    assert len(out) == 0


def test_read_weight_data_multiple_rows(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25", "04.11.25"],
        "weight": [80.0, 79.5],
        "time": ["08:00:00", "08:00:00"],
        "rr_syst": [120, 130],
        "rr_diast": [80, 85],
        "heart_rate": [70, 75],
    })

    fn = write_excel(tmp_path, df)
    out = read_weight_data(fn)

    assert len(out) == 2
    assert list(out["weight"]) == [80.0, 79.5]
