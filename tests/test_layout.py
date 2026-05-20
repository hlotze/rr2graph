"""Unit tests for rr2graph.layout."""

import pytest

from rr2graph.layout import get_needed_fig_and_axs_array


def test_layout_one_month():
    """Validate the single-month A4 landscape layout."""
    fig, axs = get_needed_fig_and_axs_array(1)

    assert len(axs) == 3  # Single-row layout returns a flat axes array.
    assert fig.get_figwidth() == pytest.approx(11.69)
    assert fig.get_figheight() == pytest.approx(8.27 / 3, rel=0.1)


def test_layout_two_months():
    """Validate the two-month A4 landscape layout."""
    fig, axs = get_needed_fig_and_axs_array(2)

    assert len(axs) == 2  # Two layout rows.
    assert len(axs[0]) == 3  # Three plot columns.
    assert fig.get_figwidth() == pytest.approx(11.69)
    assert fig.get_figheight() == pytest.approx(8.27 * 2 / 3, rel=0.1)


def test_layout_three_months():
    """Validate the three-month A4 landscape layout."""
    fig, axs = get_needed_fig_and_axs_array(3)

    assert len(axs) == 3
    assert len(axs[0]) == 3
    assert fig.get_figwidth() == pytest.approx(11.69)
    assert fig.get_figheight() == pytest.approx(8.27 * 3 / 3, rel=0.1)


def test_layout_four_to_six_months():
    """Validate A3 portrait layouts for four to six months."""
    for n in [4, 5, 6]:
        fig, axs = get_needed_fig_and_axs_array(n)

        assert len(axs) == n
        assert len(axs[0]) == 3
        assert fig.get_figwidth() == pytest.approx(11.69)
        assert fig.get_figheight() == pytest.approx(16.54 * n / 6, rel=0.1)


def test_layout_invalid_months():
    """Reject unsupported month counts."""
    with pytest.raises(SystemExit):
        get_needed_fig_and_axs_array(0)

    with pytest.raises(SystemExit):
        get_needed_fig_and_axs_array(7)
