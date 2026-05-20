"""Shared pytest fixtures and test utilities for rr2graph."""

from datetime import datetime

import pandas as pd
import pytest
import xlsxwriter

from pathlib import Path


def write_excel(tmp_path: Path, df: pd.DataFrame) -> Path:
    """
    Write a temporary Excel workbook for integration tests.

    Args:
        tmp_path:
            Temporary pytest directory.

        df:
            Dataframe written into the workbook.

    Returns:
        Path:
            Path to the generated Excel workbook.
    """
    fn = tmp_path / "test.xlsx"

    workbook = xlsxwriter.Workbook(fn)
    worksheet = workbook.add_worksheet("data")

    # Write column headers.
    for col, name in enumerate(df.columns):
        worksheet.write(0, col, name)

    # Write dataframe values as raw worksheet data.
    for row in range(len(df)):
        for col, name in enumerate(df.columns):
            worksheet.write(row + 1, col, df.iloc[row, col])

    workbook.close()
    return fn


@pytest.fixture
def df_heart_sample():
    """Provide a small RR dataframe for monthly plot tests."""
    data = {
        "date_time": [
            datetime(2024, 12, 31, 8, 0),
            datetime(2025, 1, 1, 9, 0),
            datetime(2025, 2, 15, 10, 0),
            datetime(2025, 3, 20, 11, 0),
        ],
        "rr_syst": [120, 125, 130, 128],
        "rr_diast": [80, 82, 85, 84],
        "heart_rate": [70, 72, 75, 74],
    }
    return pd.DataFrame(data)


@pytest.fixture
def df_weight_sample():
    """Provide a small weight dataframe for monthly plot tests."""
    data = {
        "date": [
            datetime(2024, 12, 31),
            datetime(2025, 1, 1),
            datetime(2025, 2, 15),
            datetime(2025, 3, 20),
        ],
        "weight": [80.0, 79.5, 79.0, 78.5],
    }
    return pd.DataFrame(data)
