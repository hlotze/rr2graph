"""collects all axs with plots and saves figures for pdf, png, svg diagrams"""

import os

# from typing import List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# import pandas as pd
# from .helpers import ensure_output_dirs
from .layout import get_needed_fig_and_axs_array
from .monthly import gen_req_plot_type


def generate_monthly_plots(
    plot_type, num_of_months, df_heart, df_weight, out_dir
) -> list[str]:
    """generate a mothly plot
    i.e. one row of 3 axs for
    e.g. scatter, histo, histo"""
    fig, axs = get_needed_fig_and_axs_array(num_of_months)

    fn_base = gen_req_plot_type(
        plot_type,
        num_of_months,
        df_heart,
        df_weight,
        axs,
    )

    # sicher stellen Unterordner png/, pdf/, svg/
    formats = ("png", "pdf", "svg")
    files = []

    for ext in formats:
        subdir = os.path.join(out_dir, ext)
        os.makedirs(subdir, exist_ok=True)

        fn = os.path.join(subdir, f"{fn_base}.{ext}")
        fig.savefig(fn)
        files.append(fn)

    # DummyFig nicht schließen
    if isinstance(fig, Figure):
        plt.close(fig)

    return files
