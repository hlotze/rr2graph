"""
Command line interface for rr2graph.

This module provides the primary command line entry points used to
execute rr2graph workflows.

The CLI supports:
    - importing RR Excel datasets
    - generating statistical graph visualizations
    - exporting generated plots
    - loading optional YAML configuration files
    - generating synthetic test datasets
    - displaying runtime and configuration information

The module is intended for both interactive usage and automated
execution environments such as CI pipelines or scheduled jobs.
"""

import argparse
from pathlib import Path
from typing import Sequence
from . import __version__, XLSX_FN, NUM_OF_MONTHS, OUTPUT_DIR
from .helpers import (
    valid_month,
    load_config,
    print_info,
    GREEN,
    YELLOW,
    BLUE,
    # MAGENTA,
    CYAN,
    RESET,
)
from .io import read_heart_data, read_weight_data, generate_test_data_xlsx
from .orchestrator import generate_monthly_plots


def parse_args() -> argparse.Namespace:
    """
    Parse and validate command line arguments.

    Creates the rr2graph command line parser and registers all
    supported command line options.

    Supported options include:
        - Excel input file selection
        - output directory configuration
        - month range filtering
        - YAML configuration loading
        - test data generation
        - runtime information display

    Returns:
        argparse.Namespace:
            Parsed command line arguments.

    Raises:
        argparse.ArgumentError:
            Raised when invalid command line arguments are provided.

    Examples:
        Generate plots from a custom Excel file:

            python -m rr2graph.cli --excel rr_data.xlsx

        Generate plots for the last three months:

            python -m rr2graph.cli --num_of_months 3

        Use a custom YAML configuration:

            python -m rr2graph.cli --config config.yml
    """
    parser = argparse.ArgumentParser(
        description="Load Excel datasets and generate RR visualization plots."
    )

    parser.add_argument(
        "-e",
        "--excel",
        type=str,
        default=None,
        help=f"Path to the Excel input file (default: {XLSX_FN})",
    )

    parser.add_argument(
        "-n",
        "--num_of_months",
        type=valid_month,
        default=None,
        help=f"Number of months to visualize: 1-6 (default: {NUM_OF_MONTHS})",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help=f"Output directory for generated plots (default: {OUTPUT_DIR})",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Path to an optional YAML configuration file",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"rr2graph {__version__}"
    )

    parser.add_argument(
        "-g",
        "--generate-test-data",
        action="store_true",
        help="Generate test_rr_data.xlsx and exit the program",
    )

    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Display runtime and configuration information",
    )
    return parser.parse_args()


def main() -> None:
    """
    Execute the rr2graph command line workflow.

    This function coordinates the complete runtime execution flow:

        1. Parse command line arguments
        2. Load optional configuration values
        3. Read RR source datasets
        4. Generate graph visualizations
        5. Export generated plots
        6. Display execution results

    The workflow supports multiple plot generation strategies,
    including:
        - histogram
        - violin
        - box_swarm

    Raises:
        FileNotFoundError:
            Raised when the configured Excel source file does not exist.

        ValueError:
            Raised when invalid configuration values are detected.

        RuntimeError:
            Raised when plot generation fails.

    Examples:
        Generate all plots using default configuration:

            python -m rr2graph.cli

        Generate plots from a specific Excel dataset:

            python -m rr2graph.cli --excel rr_data.xlsx

        Generate plots using a custom output directory:

            python -m rr2graph.cli --output ./plots

        Generate synthetic test datasets:

            python -m rr2graph.cli --generate-test-data
    """
    args = parse_args()

    if args.info:
        print_info()
        return

    if args.generate_test_data:
        print("→ Generating test_rr_data.xlsx …")
        generate_test_data_xlsx()
        print("✓ Test dataset generated.")
        return

    # ------------------------------------------------------------------
    # Load configuration
    # ------------------------------------------------------------------
    cfg = load_config(args.config)

    excel_fn: str | Path = args.excel or cfg.get("excel", XLSX_FN)
    num_months: int = args.num_of_months or cfg.get("num_of_months", NUM_OF_MONTHS)
    out_dir: str | Path = args.output or cfg.get("output", OUTPUT_DIR)

    # ------------------------------------------------------------------
    # Load source datasets
    # ------------------------------------------------------------------
    df_heart = read_heart_data(excel_fn)
    df_weight = read_weight_data(excel_fn)

    print("Heart rows read:", len(df_heart))
    print("Weight rows read:", len(df_weight))
    print()

    print(f"{CYAN}→ Excel file:{RESET} {excel_fn}")
    print(f"{CYAN}→ Months:{RESET} {num_months}")
    print(f"{CYAN}→ Output directory:{RESET} {out_dir}")
    print()

    # ------------------------------------------------------------------
    # Generate visualization outputs
    # ------------------------------------------------------------------
    # Iterate through all configured visualization strategies.
    plot_types: Sequence[str] = ("histogram", "violin", "box_swarm")

    for plot_type in plot_types:
        print(f"{YELLOW}Generating {plot_type} plots…{RESET}")
        files: Sequence[str] = generate_monthly_plots(
            plot_type, num_months, df_heart, df_weight, out_dir
        )

        print(f"{GREEN}Generated {plot_type} plots stored at:{RESET}")
        for f in files:
            print(f"{BLUE}-- {f}{RESET}")
        print()


if __name__ == "__main__":
    main()
