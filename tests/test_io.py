"""Unit tests for rr2graph.io."""

from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from rr2graph.io import (
    parse_excel_date,
    read_heart_data,
    read_weight_data,
)

from pathlib import Path


# Helper function for temporary Excel workbooks.

def write_excel(tmp_path: Path, df: pd.DataFrame) -> Path:
    """Write a temporary Excel workbook for integration tests."""
    fn = tmp_path / "test.xlsx"
    df.to_excel(fn, sheet_name="data", index=False)
    return fn


# ---------------------------------------------------------
# _parse_excel_date()
# ---------------------------------------------------------

def test_parse_excel_date_dd_mm_yy():
    assert parse_excel_date("03.11.25") == pd.Timestamp(2025, 11, 3)


def test_parse_excel_date_dd_mm_yyyy():
    assert parse_excel_date("03.11.2025") == pd.Timestamp(2025, 11, 3)


def test_parse_excel_date_iso_dayfirst_behavior():
    """Ensure ISO date strings are parsed correctly."""
    # ISO dates must preserve YYYY-MM-DD semantics.
    assert parse_excel_date("2025-11-03") == pd.Timestamp(2025, 11, 3)


def test_parse_excel_date_excel_int():
    """Validate Excel serial date conversion."""
    # Excel serial date 45231 maps to 2023-11-01.
    assert parse_excel_date(45231) == pd.Timestamp(year=2023, month=11, day=1)


def test_parse_excel_date_excel_float():
    assert parse_excel_date(45231.0) == pd.Timestamp(year=2023, month=11, day=1)


def test_parse_excel_date_excel_str():
    assert parse_excel_date("45231") == pd.Timestamp(year=2023, month=11, day=1)


def test_parse_excel_date_timestamp_passthrough():
    ts = pd.Timestamp("2025-11-03")
    assert parse_excel_date(ts) == ts


def test_parse_excel_date_invalid():
    assert pd.isna(parse_excel_date("not-a-date"))


def test_parse_excel_date_nan_float():
    assert pd.isna(parse_excel_date(float("nan")))


def test_parse_excel_date_str_with_spaces():
    assert parse_excel_date("   45231   ") == pd.Timestamp(2023, 11, 1)


def test_parse_excel_date_str_with_leading_zeros():
    assert parse_excel_date("00045231") == pd.Timestamp(2023, 11, 1)


def test_parse_excel_date_timestamp_in_range():
    ts = pd.Timestamp("2020-01-01")
    assert parse_excel_date(ts) == pd.Timestamp("2020-01-01")


def test_parse_excel_date_excel_nan_int_branch():
    """Cover the float conversion fallback branch."""
    # Cover the float conversion branch with a custom float subclass.
    class WeirdFloat(float):
        pass
    val = WeirdFloat(123.456)
    expected = pd.Timestamp("1899-12-30") + pd.Timedelta(days=123.456)
    assert abs(parse_excel_date(val) - expected) < pd.Timedelta(microseconds=1)


def test_parse_excel_date_str_not_digit():
    """Reject non-digit Excel serial strings."""
    # Trigger the non-digit string branch.
    assert pd.isna(parse_excel_date("45 231"))


def test_parse_excel_date_timestamp_delta_zero():
    """Preserve timestamps near the Excel epoch."""
    # Preserve timestamps at the Excel epoch boundary.
    ts = pd.Timestamp("1899-12-30")
    assert parse_excel_date(ts) == ts


def test_parse_excel_date_timestamp_delta_too_large():
    """Preserve timestamps outside Excel serial date ranges."""
    # Preserve timestamps outside supported Excel date ranges.
    ts = pd.Timestamp("2100-01-01")
    assert parse_excel_date(ts) == ts


def test_parse_excel_date_float_non_nan_branch():
    class MyFloat(float):
        pass
    val = MyFloat(123.0)
    assert parse_excel_date(val) == pd.Timestamp("1899-12-30") + pd.Timedelta(days=123)


def test_parse_excel_date_str_not_digit_else_branch():
    assert pd.isna(parse_excel_date("abc"))


def test_parse_excel_date_timestamp_delta_one():
    ts = pd.Timestamp("1899-12-31")
    assert parse_excel_date(ts) == ts


def test_parse_excel_date_iso_datetime():
    assert parse_excel_date("2025-11-03 08:30:00") == pd.Timestamp(2025, 11, 3, 8, 30)


def test_parse_excel_date_exception_branch():
    """Handle invalid date-like objects gracefully."""
    class Boom:
        @property
        def year(self):
            raise ValueError("boom")

    result = parse_excel_date(Boom())
    assert pd.isna(result)

def test_parse_excel_date_python_datetime():
    dt = datetime(2025, 11, 3, 8, 30)
    assert parse_excel_date(dt) == pd.Timestamp(dt)


def test_parse_excel_date_numpy_datetime64():
    nd = np.datetime64("2025-11-03")
    assert parse_excel_date(nd) == pd.Timestamp("2025-11-03")


def test_parse_excel_date_empty_string():
    assert parse_excel_date("") is None


# ---------------------------------------------------------
# _to_pydate()
# ---------------------------------------------------------


def test_to_pydate_variants():
    """Validate datetime-to-date conversion helpers."""
    from rr2graph.io import _to_pydate

    # Standard datetime instance.
    dt = datetime(2025, 1, 1, 8, 0)
    assert _to_pydate(dt) == dt.date()

    # NumPy datetime64 instance.
    nd = np.datetime64("2025-01-01")
    assert _to_pydate(nd) == datetime(2025, 1, 1).date()

    # Unsupported values fall back unchanged.
    assert _to_pydate("abc") == "abc"

# ---------------------------------------------------------
# read_heart_data()
# ---------------------------------------------------------

def test_read_heart_data_parses_valid_row(tmp_path):
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
    """Drop heart data rows with invalid timestamps."""
    df = pd.DataFrame({
        "date": ["03.11.25"],
        "time": [""],  # Invalid timestamp.
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


def test_read_heart_data_invalid_date(tmp_path):
    """Drop heart data rows with invalid dates."""
    df = pd.DataFrame({
        "date": ["not-a-date"],
        "time": ["08:00:00"],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
        "weight": [80.0],
    })

    fn = write_excel(tmp_path, df)
    out = read_heart_data(fn)

    assert len(out) == 0


def test_read_heart_data_dropna_executes(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25", "04.11.25"],
        "time": ["08:00:00", ""],  # Second row will be dropped.
        "rr_syst": [120, 130],
        "rr_diast": [80, 85],
        "heart_rate": [70, 75],
        "weight": [80.0, 79.5],
    })

    fn = write_excel(tmp_path, df)
    out = read_heart_data(fn)

    assert len(out) == 1


def test_read_heart_data_int_conversion(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25"],
        "time": ["08:00:00"],
        "rr_syst": ["120"],  # Stored as strings.
        "rr_diast": ["80"],
        "heart_rate": ["70"],
        "weight": ["80.0"],
    })

    fn = write_excel(tmp_path, df)
    out = read_heart_data(fn)

    assert out["rr_syst"].dtype == "int64"
    assert out["rr_diast"].dtype == "int64"


# ---------------------------------------------------------
# read_weight_data()
# ---------------------------------------------------------

def test_read_weight_data_parses_valid_row(tmp_path):
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
    """Drop weight rows with invalid numeric values."""
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


def test_read_weight_data_invalid_date(tmp_path):
    """Drop weight rows with invalid dates."""
    df = pd.DataFrame({
        "date": ["not-a-date"],
        "weight": [80.0],
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


def test_read_weight_data_drops_invalid_rows(tmp_path):
    df = pd.DataFrame({
        "date": ["03.11.25", "not-a-date"],
        "weight": [80.0, 79.5],
        "time": ["08:00:00", "08:00:00"],
        "rr_syst": [120, 130],
        "rr_diast": [80, 85],
        "heart_rate": [70, 75],
    })

    fn = write_excel(tmp_path, df)
    out = read_weight_data(fn)

    assert len(out) == 1
    assert out["weight"].iloc[0] == 80.0


def test_read_heart_data_full(tmp_path):
    fn = tmp_path / "heart.xlsx"

    df = pd.DataFrame({
        "date": ["01.01.2025", "02.01.2025"],
        "time": ["08:00:00", ""],  # Second row will be dropped.
        "rr_syst": ["120", "130"],
        "rr_diast": ["80", "85"],
        "heart_rate": ["70", "75"],
        "weight": ["80", "80"],  # Converted during processing.
    })

    df.to_excel(fn, sheet_name="data", index=False)

    out = read_heart_data(fn)

    # Only the first row remains after cleanup.
    assert len(out) == 1

    # Numeric columns must be converted correctly.
    assert out["rr_syst"].dtype == "int64"
    assert out["rr_diast"].dtype == "int64"
    assert out["heart_rate"].dtype == "int64"

    # Combined datetime column must exist.
    assert "date_time" in out.columns


def test_read_weight_data_full(tmp_path):
    fn = tmp_path / "weight.xlsx"

    df = pd.DataFrame({
        "date": ["01.01.2025", "02.01.2025"],
        "time": ["08:00:00", "09:00:00"],
        "rr_syst": ["120", "130"],
        "rr_diast": ["80", "85"],
        "heart_rate": ["70", "75"],
        "weight": ["80.5", "81.0"],
    })

    df.to_excel(fn, sheet_name="data", index=False)

    out = read_weight_data(fn)

    assert len(out) == 2

    # Ensure timestamp filtering succeeds.
    assert isinstance(out["date"].iloc[0], pd.Timestamp)

    # Ensure numeric conversion succeeds.
    assert out["weight"].dtype == "float64"

    # Ensure ISO week column exists.
    assert "week" in out.columns
