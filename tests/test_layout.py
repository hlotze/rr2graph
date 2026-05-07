import pytest
from rr2graph.layout import get_needed_fig_and_axs_array


def test_layout_one_month():
    """1 Monat → 1 Zeile, 3 Spalten, A4 Landscape / 1/3 Höhe."""
    fig, axs = get_needed_fig_and_axs_array(1)

    assert len(axs) == 3                     # 1x3 → axs ist 1D-Liste mit 3 Elementen
    assert fig.get_figwidth() == pytest.approx(11.69)
    assert fig.get_figheight() == pytest.approx(8.27 / 3, rel=0.1)


def test_layout_two_months():
    """2 Monate → 2 Zeilen, 3 Spalten, A4 Landscape."""
    fig, axs = get_needed_fig_and_axs_array(2)

    assert len(axs) == 2                     # 2 Zeilen
    assert len(axs[0]) == 3                  # 3 Spalten
    assert fig.get_figwidth() == pytest.approx(11.69)
    assert fig.get_figheight() == pytest.approx(8.27 * 2 / 3, rel=0.1)


def test_layout_three_months():
    """3 Monate → 3 Zeilen, 3 Spalten, A4 Landscape."""
    fig, axs = get_needed_fig_and_axs_array(3)

    assert len(axs) == 3
    assert len(axs[0]) == 3
    assert fig.get_figwidth() == pytest.approx(11.69)
    assert fig.get_figheight() == pytest.approx(8.27 * 3 / 3, rel=0.1)


def test_layout_four_to_six_months():
    """4–6 Monate → A3 Portrait."""
    for n in [4, 5, 6]:
        fig, axs = get_needed_fig_and_axs_array(n)

        assert len(axs) == n
        assert len(axs[0]) == 3
        assert fig.get_figwidth() == pytest.approx(11.69)
        assert fig.get_figheight() == pytest.approx(16.54 * n / 6, rel=0.1)


def test_layout_invalid_months():
    """Ungültige Monatszahl → SystemExit."""
    with pytest.raises(SystemExit):
        get_needed_fig_and_axs_array(0)

    with pytest.raises(SystemExit):
        get_needed_fig_and_axs_array(7)
