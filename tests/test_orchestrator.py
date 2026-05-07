from datetime import datetime

# import os
import pytest
import pandas as pd

from rr2graph.orchestrator import generate_monthly_plots


class DummyFig:
    """Fake Matplotlib Figure, um savefig zu mocken."""
    def __init__(self):
        self.saved_files = []

    def savefig(self, fn):
        self.saved_files.append(fn)

    def close(self):
        pass


def test_generate_monthly_plots_creates_three_files(tmp_path, monkeypatch):
    """Testet, ob PNG, PDF und SVG erzeugt werden."""

    # Fake-Figure zurückgeben
    dummy_fig = DummyFig()

    def fake_get_fig_and_axs_array(num):
        axs = [[None, None, None] for _ in range(num)]
        return dummy_fig, axs

    def fake_gen_req_plot_type(plot_type, num, df_h, df_w, axs):
        return "(2025-01__2025-03 3 months) per month data and histogram"

    # Monkeypatching
    monkeypatch.setattr(
        "rr2graph.orchestrator.get_needed_fig_and_axs_array",
        fake_get_fig_and_axs_array,
    )
    monkeypatch.setattr(
        "rr2graph.orchestrator.gen_req_plot_type",
        fake_gen_req_plot_type,
    )

    # Dummy-Daten
    df_heart = pd.DataFrame({
        "date_time": [
            datetime(2025, 1, 1),
            datetime(2025, 2, 1),
            datetime(2025, 3, 1),
        ],
        "rr_syst": [120, 125, 130],
        "rr_diast": [80, 82, 85],
        "heart_rate": [70, 72, 75],
    })

    df_weight = pd.DataFrame({
        "date": [
            datetime(2025, 1, 1),
            datetime(2025, 2, 1),
            datetime(2025, 3, 1),
        ],
        "weight": [80.0, 79.5, 79.0],
    })

    out_dir = tmp_path / "plots"

    files = generate_monthly_plots(
        "histogram",
        3,
        df_heart,
        df_weight,
        str(out_dir),
    )

    # Es müssen 3 Dateien erzeugt werden
    assert len(files) == 3

    # Alle Endungen müssen vorkommen
    assert any(f.endswith(".png") for f in files)
    assert any(f.endswith(".pdf") for f in files)
    assert any(f.endswith(".svg") for f in files)

    # Dateien müssen im richtigen Ordner liegen
    assert (out_dir / "png").exists()
    assert (out_dir / "pdf").exists()
    assert (out_dir / "svg").exists()

    # DummyFig muss savefig dreimal aufgerufen haben
    assert len(dummy_fig.saved_files) == 3


def test_generate_monthly_plots_invalid_months():
    """Ungültige Monatszahl → SystemExit."""
    df = pd.DataFrame({
        "date_time": [datetime(2025, 1, 1)],
        "rr_syst": [120],
        "rr_diast": [80],
        "heart_rate": [70],
    })
    df_w = pd.DataFrame({
        "date": [datetime(2025, 1, 1)],
        "weight": [80.0],
    })

    with pytest.raises(SystemExit):
        generate_monthly_plots("histogram", 0, df, df_w, "plots")

    with pytest.raises(SystemExit):
        generate_monthly_plots("histogram", 7, df, df_w, "plots")
