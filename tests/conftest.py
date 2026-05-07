from datetime import datetime  # , time

import pandas as pd
import xlsxwriter

import pytest


def write_excel(tmp_path, df):
    fn = tmp_path / "test.xlsx"

    workbook = xlsxwriter.Workbook(fn)
    worksheet = workbook.add_worksheet("data")

    # Header schreiben
    for col, name in enumerate(df.columns):
        worksheet.write(0, col, name)

    # Daten schreiben (als rohe Werte)
    for row in range(len(df)):
        for col, name in enumerate(df.columns):
            worksheet.write(row + 1, col, df.iloc[row, col])

    workbook.close()
    return fn


@pytest.fixture
def df_heart_sample():
    """kleiner DataFrame für Monats-Tests"""
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
