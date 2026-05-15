import pandas as pd
import numpy as np
import pytest
from datetime import datetime

from rr2graph.io import (
    parse_excel_date,
    read_heart_data,
    read_weight_data,
)


# ---------------------------------------------------------
# Hilfsfunktion zum Schreiben einer Excel-Datei
# ---------------------------------------------------------

def write_excel(tmp_path, df):
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
    # ISO-Date wird korrekt als YYYY-MM-DD interpretiert (3. November 2025)
    assert parse_excel_date("2025-11-03") == pd.Timestamp(2025, 11, 3)


def test_parse_excel_date_excel_int():
    # Excel-Seriendatum 45231 = 2023-11-01 (Pandas-Korrekte Interpretation)
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
    # val = float("nan") geht in except → wir brauchen einen Wert,
    # der isinstance(val, float) ist, aber pd.isna(val) == False
    class WeirdFloat(float):
        pass
    val = WeirdFloat(123.456)
    assert parse_excel_date(val) == pd.Timestamp("1899-12-30") + pd.Timedelta(days=123)


def test_parse_excel_date_str_not_digit():
    # trifft den else-Zweig von s.isdigit()
    assert pd.isna(parse_excel_date("45 231"))


def test_parse_excel_date_timestamp_delta_zero():
    # delta = 0 → trifft den unteren return val
    ts = pd.Timestamp("1899-12-30")
    assert parse_excel_date(ts) == ts


def test_parse_excel_date_timestamp_delta_too_large():
    # delta >= 60000 → trifft den unteren return val
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
    class Boom:
        @property
        def year(self):
            raise ValueError("boom")

    result = parse_excel_date(Boom())
    assert pd.isna(result)


# ---------------------------------------------------------
# _to_pydate()
# ---------------------------------------------------------


def test_to_pydate_variants():
    from rr2graph.io import _to_pydate

    # datetime
    dt = datetime(2025, 1, 1, 8, 0)
    assert _to_pydate(dt) == dt.date()

    # numpy.datetime64
    nd = np.datetime64("2025-01-01")
    assert _to_pydate(nd) == datetime(2025, 1, 1).date()

    # fallback
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


def test_read_heart_data_invalid_date(tmp_path):
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
        "time": ["08:00:00", ""],  # zweite Zeile wird gedroppt
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
        "rr_syst": ["120"],  # als STRING
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
        "time": ["08:00:00", ""],  # zweite Zeile wird gedroppt → deckt Zeile 42
        "rr_syst": ["120", "130"],
        "rr_diast": ["80", "85"],
        "heart_rate": ["70", "75"],
        "weight": ["80", "80"],  # wird später gedroppt
    })

    df.to_excel(fn, sheet_name="data", index=False)

    out = read_heart_data(fn)

    # Nur die erste Zeile bleibt übrig
    assert len(out) == 1

    # Typen wurden konvertiert → deckt Zeilen 55–56
    assert out["rr_syst"].dtype == "int64"
    assert out["rr_diast"].dtype == "int64"
    assert out["heart_rate"].dtype == "int64"

    # date_time wurde erzeugt
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

    # deckt Zeile 69 (Timestamp‑Filter)
    assert isinstance(out["date"].iloc[0], pd.Timestamp)

    # deckt Zeile 70 (to_numeric)
    assert out["weight"].dtype == "float64"

    # deckt Zeile 72 (week-Spalte)
    assert "week" in out.columns

