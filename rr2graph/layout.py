"""the layouter function generates to fig and axs-array for the plots"""

import sys
import matplotlib.pyplot as plt

# import matplotlib.axes


def get_needed_fig_and_axs_array(num_of_months: int):
    """generates the fig and axes-array for the plots"""
    # Test verlangt: ungültige Monatszahl → SystemExit
    if num_of_months < 1 or num_of_months > 6:
        raise SystemExit(f"Invalid number of months: {num_of_months}")

    a4_landscape_inches = (11.69, 8.27)
    a3_portrait_inches = (11.69, 16.54)
    width_ratio = (4, 1, 1)

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
    else:
        sys.exit(
            "Error: The number of months must be between 1 and 6 "
            "to generate the plots with the given layout."
        )
    return fig, axs
