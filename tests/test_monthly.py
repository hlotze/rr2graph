""""Tests für die rr2graph.monthly Funktionen."""

import pandas as pd
import pytest
import matplotlib.pyplot as plt

from rr2graph.monthly import (
    gen_req_plot_type,
    _ensure_output_dirs,
    _build_output_paths
)
import rr2graph.monthly as monthly


def test_ensure_output_dirs(tmp_path):
    """Testet, ob die Ausgabeordner korrekt erstellt werden."""

    dirs = _ensure_output_dirs(tmp_path)

    assert (tmp_path / "png").exists()
    assert (tmp_path / "pdf").exists()
    assert (tmp_path / "svg").exists()

    assert dirs["png"] == tmp_path / "png"
    assert dirs["pdf"] == tmp_path / "pdf"
    assert dirs["svg"] == tmp_path / "svg"


def test_build_output_paths(tmp_path):
    """Testet, ob die Dateipfade korrekt aufgebaut werden."""
    subdirs = {
        "png": tmp_path / "png",
        "pdf": tmp_path / "pdf",
        "svg": tmp_path / "svg",
    }

    paths = _build_output_paths(subdirs, "testfile")

    assert paths["png"].name == "testfile.png"
    assert paths["pdf"].name == "testfile.pdf"
    assert paths["svg"].name == "testfile.svg"


def test_row_func_violin(monkeypatch,
                         df_heart_sample,
                         df_weight_sample):
    """Testet, ob die richtige row_func
    für den Violin-Plot aufgerufen wird."""
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_violin",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]
    gen_req_plot_type("violin", 2, df_heart_sample, df_weight_sample, axs)

    assert calls == ["2025-02", "2025-03"]


def test_row_func_box_swarm(monkeypatch, df_heart_sample, df_weight_sample):
    """Testet, ob die richtige row_func
    für den Box-Swarm-Plot aufgerufen wird."""
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_box_swarm",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]
    gen_req_plot_type("box_swarm", 2, df_heart_sample, df_weight_sample, axs)

    assert calls == ["2025-02", "2025-03"]
    
    
def test_row_func_violin_called(monkeypatch, df_heart_sample, df_weight_sample):
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_violin",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]

    gen_req_plot_type(
        "violin",
        2,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    assert calls == ["2025-02", "2025-03"]


def test_row_func_box_swarm_called(monkeypatch, df_heart_sample, df_weight_sample):
    calls = []

    def fake(month, axs, df_h, df_w):
        calls.append(str(month))

    monkeypatch.setattr(
        "rr2graph.monthly.gen_row_of_3_grapics_for_one_month_box_swarm",
        fake,
    )

    axs = [[None, None, None], [None, None, None]]

    gen_req_plot_type(
        "box_swarm",
        2,
        df_heart_sample.copy(),
        df_weight_sample.copy(),
        axs,
    )

    assert calls == ["2025-02", "2025-03"]


def test_generate_monthly_plots(monkeypatch, tmp_path, df_heart_sample, df_weight_sample):

    # Fake figure + axes
    class FakeFig:
        def __init__(self):
            self.saved = []

        def savefig(self, path, format=None):
            self.saved.append((str(path), format))

        def close(self):
            pass

    fake_fig = FakeFig()
    fake_axs = [[None, None, None]]

    # Patch: Figure + Axes
    monkeypatch.setattr(
        monthly,
        "get_needed_fig_and_axs_array",
        lambda n: (fake_fig, fake_axs),
    )

    # Patch: Filename
    monkeypatch.setattr(
        monthly,
        "gen_req_plot_type",
        lambda *args, **kwargs: "testfile",
    )

    # Patch: plt.close → akzeptiert FakeFig
    monkeypatch.setattr("matplotlib.pyplot.close", lambda fig: None)

    paths = monthly.generate_monthly_plots(
        "histogram", 1, df_heart_sample, df_weight_sample, tmp_path
    )

    assert len(paths) == 3
    assert any("testfile.png" in p for p in paths)
    assert any("testfile.pdf" in p for p in paths)
    assert any("testfile.svg" in p for p in paths)


def test_gen_req_plot_type_invalid():
    df_heart = pd.DataFrame({"date_time": [], "rr_syst": [], "rr_diast": [], "heart_rate": []})
    df_weight = pd.DataFrame({"date": [], "weight": []})

    fig, axs = plt.subplots(nrows=1, ncols=3)

    with pytest.raises(KeyError):
        gen_req_plot_type("invalid_plot_type", 1, df_heart, df_weight, axs)



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


def test_row_func_called_correctly(
    monkeypatch,
    df_heart_sample,
    df_weight_sample
):
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


def test_month_filtering_respects_year_boundaries(
    df_heart_sample,
    df_weight_sample
):
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
