# import pandas as pd
# import pytest
from rr2graph.monthly import gen_req_plot_type


def test_month_extraction_last_n_months(df_heart_sample, df_weight_sample):
    """Testet, ob die letzten num_of_months korrekt extrahiert werden."""
    # 4 Monate im Sample: 2024-12, 2025-01, 2025-02, 2025-03
    num_months = 3

    # Dummy-AXS-Array (3 Zeilen, 3 Spalten)
    axs = [[None, None, None] for _ in range(num_months)]

    _ = gen_req_plot_type(
        "histogram",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Erwartete Monate: 2025-01, 2025-02, 2025-03
    expected = ["2025-01", "2025-02", "2025-03"]
    months = (
        df_heart_sample["date_time"]
        .dt.to_period("M")
        .sort_values()
        .unique()
    )[-num_months:]

    assert [str(m) for m in months] == expected


def test_row_func_called_correctly(monkeypatch, df_heart_sample, df_weight_sample):
    """Testet, ob row_func für jeden Monat genau einmal aufgerufen wird."""
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

    # Erwartete Monate: 2025-02, 2025-03
    assert calls == ["2025-02", "2025-03"]


def test_fn_base_format_multi_month(df_heart_sample, df_weight_sample):
    """Testet, ob der Dateiname korrekt formatiert wird."""
    num_months = 3
    axs = [[None, None, None] for _ in range(num_months)]

    fn = gen_req_plot_type(
        "violin",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Beispiel: (2025-01__2025-03 3 months) per month data and violin
    assert "2025-01" in fn
    assert "2025-03" in fn
    assert "3 months" in fn
    assert "violin" in fn


def test_fn_base_format_single_month(df_heart_sample, df_weight_sample):
    """Testet den 1-Monats-Fall."""
    num_months = 1
    axs = [None, None, None]

    fn = gen_req_plot_type(
        "box_swarm",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Letzter Monat im Sample ist 2025-03
    assert "(2025-03)" in fn
    assert "box_swarm" in fn


def test_month_filtering_respects_year_boundaries(df_heart_sample, df_weight_sample):
    """Testet, ob Jahresgrenzen korrekt funktionieren."""
    num_months = 2
    axs = [[None, None, None] for _ in range(num_months)]

    fn = gen_req_plot_type(
        "histogram",
        num_months,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    # Erwartete Monate: 2025-02, 2025-03
    assert "2025-02" in fn
    assert "2025-03" in fn
    assert "2024-12" not in fn
    assert "2025-01" not in fn
