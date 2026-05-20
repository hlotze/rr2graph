"""
Input/output utilities for rr2graph.

This module contains all data loading, parsing and synthetic dataset
creation utilities used by rr2graph.

The functionality includes:
    - parsing heterogeneous Excel date formats
    - loading RR measurement datasets
    - loading weight measurement datasets
    - converting pandas date objects
    - generating synthetic test datasets

The module is designed to tolerate inconsistent Excel exports and
mixed user-entered date formats.
"""

from datetime import datetime
import re

import numpy as np
import pandas as pd

# ---------------------------------------------------------
# EXCEL DATE PARSER
# ---------------------------------------------------------


def parse_excel_date(val: object) -> pd.Timestamp | pd.NaT:
    """
    Parse heterogeneous Excel-compatible date values.

    Supports multiple input formats commonly found in exported
    spreadsheet datasets.

    Supported formats:
        - Excel serial date numbers
        - ISO date strings
        - ISO datetime strings
        - German date formats
        - pandas Timestamp objects
        - numpy datetime objects

    Args:
        val:
            Raw date value originating from Excel or pandas.

    Returns:
        pd.Timestamp | pd.NaT:
            Parsed pandas timestamp or NaT if parsing fails.

    Raises:
        ValueError:
            Raised internally when invalid date formats are detected.

    Examples:
        Parse German date format:

            parse_excel_date("31.12.2025")

        Parse ISO datetime:

            parse_excel_date("2025-12-31 08:30:00")
    """
    try:
        excel_origin = pd.Timestamp("1899-12-30")

        # Case 1: Excel serial date as integer or float.
        if isinstance(val, (int, float)) and not pd.isna(val):
            return excel_origin + pd.to_timedelta(int(val), unit="D")

        # Case 2: Excel serial date as string.
        if isinstance(val, str):
            s = val.strip()
            if s.isdigit():
                return excel_origin + pd.to_timedelta(int(s), unit="D")

        # Case 3: Value already parsed as pandas Timestamp.
        if isinstance(val, pd.Timestamp):
            delta = (val - excel_origin).days
            if 1 < delta < 60000:
                return excel_origin + pd.to_timedelta(delta, unit="D")
            return val

        # Case 4: Standard date string formats.
        if isinstance(val, str):
            s = val.strip()

            # 4A: ISO datetime format.
            if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", s):
                return pd.to_datetime(s, format="%Y-%m-%d %H:%M:%S", errors="coerce")

            # 4B: ISO date format.
            if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
                return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")

            # 4C: German localized date formats.
            if re.match(r"^\d{1,2}\.\d{1,2}\.\d{2,4}$", s):
                return pd.to_datetime(s, dayfirst=True, errors="coerce")

        # Final fallback parser.
        return pd.to_datetime(val, errors="coerce")

    except Exception:  # pragma: no cover --- IGNORE ---
        return pd.NaT  # pragma: no cover --- IGNORE ---


# ---------------------------------------------------------
# DATE CONVERSION HELPERS
# ---------------------------------------------------------


def _to_pydate(val: object) -> object:
    """
    Convert pandas and numpy date objects to Python date objects.

    Args:
        val:
            Date-like object.

    Returns:
        object:
            Native Python ``date`` object or original value.
    """
    if isinstance(val, pd.Timestamp):
        return val.to_pydatetime().date()
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, np.datetime64):
        return pd.to_datetime(val).to_pydatetime().date()
    return val  # Fallback safeguard.


# -------------------------------------------------------------------------
# HEART RATE DATA IMPORT
# -------------------------------------------------------------------------


def read_heart_data(fn: str) -> pd.DataFrame:
    """
    Load RR and heart rate measurement data from Excel.

    The function normalizes inconsistent Excel date/time formats,
    converts measurement columns into numeric representations and
    generates a unified ``date_time`` column.

    Processing steps include:
        - robust date parsing
        - robust time parsing
        - invalid row filtering
        - ISO week extraction
        - datatype normalization

    Args:
        fn:
            Path to the Excel input file.

    Returns:
        pd.DataFrame:
            Cleaned RR measurement dataframe.

    Raises:
        FileNotFoundError:
            Raised when the Excel file cannot be found.

        KeyError:
            Raised when expected Excel columns are missing.

        ValueError:
            Raised when invalid data conversions occur.

    Examples:
        Load RR data:

            df = read_heart_data("rr_data.xlsx")
    """
    df = pd.read_excel(
        fn,
        sheet_name="data",
        header=0,
        dtype=str,
        engine="openpyxl",
        keep_default_na=False,
    )

    # Convert empty strings into proper NaT values.
    df.loc[df["time"].str.strip() == "", "time"] = pd.NaT

    # 2. Robustly parse date values.
    df["date"] = df["date"].apply(parse_excel_date)

    # 3. Robustly parse time values.
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S", errors="coerce").dt.time

    # 4. Remove rows without valid time values.
    df = df.dropna(subset=["time"])

    # Important: return immediately if the dataframe is empty.
    if df.empty:
        return df

    # 5. Generate unified datetime column.
    df["date_time"] = df.apply(
        lambda r: (
            datetime.combine(_to_pydate(r["date"]), r["time"])
            if pd.notna(r["date"]) and pd.notna(r["time"])
            else pd.NaT
        ),
        axis=1,
    )

    # 6. Insert ISO calendar week column.
    df.insert(0, "week", df["date_time"].dt.isocalendar().week)

    # 7. Normalize numeric datatypes.
    df["rr_syst"] = df["rr_syst"].astype("int64")
    df["rr_diast"] = df["rr_diast"].astype("int64")
    df["heart_rate"] = df["heart_rate"].astype("int64")

    # 8. Remove unused columns.
    df.drop(columns=["date", "time", "weight"], inplace=True)

    # 9. Retain only rows with valid datetime values.
    return df.dropna(subset=["date_time"])


# -------------------------------------------------------------------------
# WEIGHT DATA IMPORT
# -------------------------------------------------------------------------


def read_weight_data(fn: str) -> pd.DataFrame:
    """
    Load body weight measurements from Excel.

    The function extracts weight measurements, normalizes date values
    and converts the resulting dataset into a cleaned dataframe.

    Args:
        fn:
            Path to the Excel input file.

    Returns:
        pd.DataFrame:
            Cleaned body weight dataframe.

    Raises:
        FileNotFoundError:
            Raised when the Excel file does not exist.

        KeyError:
            Raised when required columns are missing.

    Examples:
        Load weight data:

            df = read_weight_data("rr_data.xlsx")
    """
    df = pd.read_excel(
        fn,
        sheet_name="data",
        header=0,
        keep_default_na=False,
        converters={"date": lambda x: x},
    )

    df.drop(columns=["time", "rr_syst", "rr_diast", "heart_rate"], inplace=True)

    # Robustly parse date values.
    df["date"] = df["date"].apply(parse_excel_date)
    # Weight is measured once per day and displayed
    # in the visualizations at 10:00:00.
    df["date"] = df["date"].dt.normalize() + pd.Timedelta(hours=10)

    # Retain only valid timestamp values.
    df = df[df["date"].apply(lambda x: isinstance(x, pd.Timestamp))]

    # Robustly convert weight values into floats.
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    # Retain only rows with valid weight values.
    df = df.dropna(subset=["weight"])

    # Insert ISO calendar week column.
    df.insert(0, "week", df["date"].dt.isocalendar().week)

    return df


# ---------------------------------------------------------
# TEST DATA GENERATOR
# ---------------------------------------------------------


def generate_test_data_xlsx() -> None:  # pragma: no cover
    """
    Generate a synthetic RR Excel dataset for testing.

    The generated dataset simulates approximately six months of
    RR measurements and body weight values.

    Generated characteristics include:
        - clustered measurement times
        - realistic blood pressure ranges
        - randomized outliers
        - varying heart rates

    The resulting Excel file is written to:

        ``test_rr_data.xlsx``

    Returns:
        None

    Examples:
        Generate synthetic test data:

            generate_test_data_xlsx()
    """

    # Generate realistic clustered measurement times.
    def random_time_cluster():
        cluster = np.random.choice(["morning", "noon", "evening"], p=[0.45, 0.25, 0.30])
        if cluster == "morning":
            hour = np.random.randint(6, 10)
        elif cluster == "noon":
            hour = np.random.randint(12, 15)
        else:
            hour = np.random.randint(18, 22)
        minute = np.random.choice(range(0, 60, 10))
        return pd.to_datetime(f"{hour:02d}:{minute:02d}:00").time()

    # Generate realistic RR values including statistical outliers.
    def rr_with_outliers():
        syst = np.random.randint(110, 135)
        diast = np.random.randint(65, 85)
        hr = np.random.randint(60, 95)
        if np.random.rand() < 0.05:
            syst += np.random.randint(15, 30)
            diast += np.random.randint(10, 20)
            hr += np.random.randint(15, 30)
        if np.random.rand() < 0.03:
            syst += np.random.randint(5, 15)
            diast += np.random.randint(0, 10)
            hr += np.random.randint(20, 40)
        if np.random.rand() < 0.02:
            syst += np.random.randint(20, 40)
            diast += np.random.randint(10, 25)
            hr += np.random.randint(10, 25)
        return syst, diast, hr

    # Build synthetic RR measurement records.
    records = []
    days = pd.date_range(
        start=pd.Timestamp.now() - pd.DateOffset(months=6),
        end=pd.Timestamp.now(),
        freq="D",
    )

    weights = 60 + np.random.normal(loc=0, scale=1.5, size=len(days))
    df_weight = pd.DataFrame({"date": days, "weight": weights.round(1)})

    for d in days:
        n = np.random.randint(2, 5)
        for _ in range(n):
            t = random_time_cluster()
            syst, diast, hr = rr_with_outliers()
            records.append(
                {
                    "date": d,
                    "time": t,
                    "rr_syst": syst,
                    "rr_diast": diast,
                    "heart_rate": hr,
                }
            )

    df_rr = pd.DataFrame(records)
    df = df_rr.merge(df_weight, on="date", how="left")
    df["weight"] = df.groupby("date")["weight"].transform(
        lambda x: [x.iloc[0]] + [np.nan] * (len(x) - 1)
    )
    df["date"] = df["date"].dt.strftime("%d.%m.%Y")
    df["time"] = df["time"].astype(str)
    df = df[["date", "weight", "time", "rr_syst", "rr_diast", "heart_rate"]]
    df.to_excel("test_rr_data.xlsx", sheet_name="data", index=False)
    print("Finished! File created: test_rr_data.xlsx")
    print(df.head())
