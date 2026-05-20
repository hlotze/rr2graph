"""
Plot orchestration and export management for rr2graph.

This module coordinates the complete visualization generation workflow.

Responsibilities include:
    - figure and axes allocation
    - plot type dispatching
    - export orchestration
    - multi-format rendering
    - matplotlib resource cleanup

The orchestrator acts as the central integration layer between
plot generation modules and export handling.
"""

import os

import matplotlib

# Use a non-interactive backend for headless rendering environments.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import ensure_output_dirs
from .layout import get_needed_fig_and_axs_array
from .monthly import gen_req_plot_type


def generate_monthly_plots(
    plot_type: str,
    num_of_months: int,
    df_heart,
    df_weight,
    out_dir: str,
) -> list[str]:
    """
    Generate and export monthly RR visualization plots.

    This function coordinates the complete rendering pipeline for a
    requested visualization strategy.

    Workflow steps:
        1. Allocate figure and axes layout
        2. Dispatch requested plot generator
        3. Render matplotlib figure
        4. Export all configured output formats
        5. Release matplotlib resources

    Supported export formats:
        - PNG
        - PDF
        - SVG

    Args:
        plot_type:
            Requested visualization strategy.

        num_of_months:
            Number of months to visualize.

        df_heart:
            RR measurement dataframe.

        df_weight:
            Weight measurement dataframe.

        out_dir:
            Base output directory.

    Returns:
        list[str]:
            List of generated output file paths.

    Raises:
        ValueError:
            Raised when an unsupported plot type is requested.

        OSError:
            Raised when export directories or files cannot be created.

        RuntimeError:
            Raised when matplotlib rendering fails.

    Examples:
        Generate violin plots:

            generate_monthly_plots(
                "violin",
                3,
                df_heart,
                df_weight,
                "./plots",
            )
    """
    # Allocate matplotlib figure and axis grid.
    fig, axs = get_needed_fig_and_axs_array(num_of_months)

    # Dispatch the requested visualization strategy.
    fn_base = gen_req_plot_type(
        plot_type,
        num_of_months,
        df_heart,
        df_weight,
        axs,
    )

    # Ensure export directory structure exists.
    ensure_output_dirs(out_dir)
    formats = ("png", "pdf", "svg")
    files = []

    # Export the generated figure into all supported formats.
    for ext in formats:
        subdir = os.path.join(out_dir, ext)
        os.makedirs(subdir, exist_ok=True)

        fn = os.path.join(subdir, f"{fn_base}.{ext}")
        fig.savefig(fn)
        files.append(fn)

    # Release matplotlib figure resources.
    if isinstance(fig, Figure):
        plt.close(fig)

    return files
