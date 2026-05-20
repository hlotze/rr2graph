"""
Matplotlib layout allocation utilities for rr2graph.

This module contains helper functionality responsible for generating
figure and axes layouts used throughout the rr2graph visualization
pipeline.

Responsibilities include:
    - dynamic subplot allocation
    - adaptive page sizing
    - layout normalization
    - rendering configuration
    - monthly dashboard scaling

The layout generator dynamically adjusts the figure geometry depending
on the configured number of rendered months.
"""

import sys

import matplotlib

# Use a non-interactive backend for automated rendering environments.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_needed_fig_and_axs_array(num_of_months: int):
    """
    Allocate a matplotlib figure and subplot grid.

    The generated layout dynamically adapts to the requested number
    of months.

    Layout strategies:
        - 1 month  -> compact A4 landscape layout
        - 2-3 months -> scaled A4 landscape layout
        - 4-6 months -> A3 portrait layout

    All layouts use:
        - constrained layout rendering
        - shared y-axis scaling
        - fixed subplot width ratios
        - high-resolution export settings

    Args:
        num_of_months:
            Number of months to visualize.

    Returns:
        tuple:
            Matplotlib figure and axes array.

    Raises:
        SystemExit:
            Raised when the requested month count is outside the
            supported range of 1-6.

    Examples:
        Allocate a layout for three months:

            fig, axs = get_needed_fig_and_axs_array(3)
    """
    # Validate supported month range.
    if num_of_months < 1 or num_of_months > 6:
        raise SystemExit(f"Invalid number of months: {num_of_months}")

    # Standardized print-oriented layout dimensions.
    a4_landscape_inches = (11.69, 8.27)
    a3_portrait_inches = (11.69, 16.54)
    width_ratio = (4, 1, 1)

    # Single-month compact dashboard layout.
    if num_of_months == 1:
        fig, axs = plt.subplots(
            nrows=1,
            ncols=3,
            figsize=(a4_landscape_inches[0], a4_landscape_inches[1] * 1 / 3),
            dpi=600,
            sharey=True,
            width_ratios=width_ratio,
            layout="constrained",
        )
    # Multi-row A4 dashboard layout.
    elif 2 <= num_of_months < 4:
        fig, axs = plt.subplots(
            nrows=num_of_months,
            ncols=3,
            figsize=(
                a4_landscape_inches[0],
                a4_landscape_inches[1] * num_of_months / 3,
            ),
            dpi=600,
            sharey=True,
            width_ratios=width_ratio,
            layout="constrained",
        )
    # Extended A3 dashboard layout for larger month ranges.
    elif num_of_months <= 6:
        fig, axs = plt.subplots(
            nrows=num_of_months,
            ncols=3,
            figsize=(a3_portrait_inches[0], a3_portrait_inches[1] * num_of_months / 6),
            dpi=600,
            sharey=True,
            width_ratios=width_ratio,
            layout="constrained",
        )
    else:  # pragma: no cover
        sys.exit(
            "Error: num_of_months must be between 1 and 6 "
            "to generate a valid rr2graph layout."
        )
    # Return the fully allocated matplotlib layout.
    return fig, axs
