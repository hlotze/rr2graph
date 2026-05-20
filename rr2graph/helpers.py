"""
Helper utilities for rr2graph.

This module provides shared helper functionality used throughout the
rr2graph package.

The included functionality covers:
    - configuration loading
    - validation helpers
    - filesystem utilities
    - histogram bin calculations
    - plotting tick generation
    - runtime environment inspection
    - ANSI terminal color constants

The helpers are intentionally lightweight and reusable across multiple
subsystems.
"""

import os
import sys
import platform

import argparse
import yaml
import numpy as np
import pandas as pd

from rr2graph import __file__ as pkg_file
from . import __version__

CYAN: str = "\033[96m"
GREEN: str = "\033[92m"
YELLOW: str = "\033[93m"
RESET: str = "\033[0m"
BLUE: str = "\033[94m"
MAGENTA: str = "\033[95m"


def valid_month(value: str | int) -> int:
    """
    Validate the configured month range.

    The CLI currently supports a month range between one and six months.

    Args:
        value:
            Raw command line argument value.

    Returns:
        int:
            Validated month count.

    Raises:
        argparse.ArgumentTypeError:
            Raised when the provided value is not numeric or outside
            the supported range.

    Examples:
        Validate a valid month value:

            valid_month("3")
    """
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Months must be a numeric value between 1 and 6."
        )
    if ivalue < 1 or ivalue > 6:
        raise argparse.ArgumentTypeError("Months must be between 1 and 6.")
    return ivalue


def load_config(path: str | None) -> dict:
    """
    Load a YAML configuration file.

    The configuration loader safely parses YAML content and returns
    a normalized dictionary representation.

    Missing configuration files are tolerated and result in an empty
    configuration object.

    Args:
        path:
            Optional path to a YAML configuration file.

    Returns:
        dict:
            Parsed configuration dictionary.

    Raises:
        yaml.YAMLError:
            Raised when invalid YAML syntax is encountered.

    Examples:
        Load a configuration file:

            cfg = load_config("config.yaml")
    """
    if path is None:
        return {}
    if not os.path.exists(path):
        print(f"[WARN] Config file not found: {path} — ignoring it.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def ensure_output_dirs(base: str) -> None:
    """
    Ensure all required output directories exist.

    The function creates the configured base output directory and all
    required export subdirectories.

    Generated directories include:
        - png
        - pdf
        - svg

    Args:
        base:
            Base output directory.

    Returns:
        None

    Raises:
        OSError:
            Raised when directory creation fails.
    """
    subdirs = ["png", "pdf", "svg"]
    os.makedirs(base, exist_ok=True)
    for sd in subdirs:
        os.makedirs(os.path.join(base, sd), exist_ok=True)


def binwidth_2_bins(data: np.ndarray, binwidth: int) -> np.ndarray:
    """
    Calculate histogram bin boundaries.

    Generates a normalized numpy bin array based on the provided
    dataset and histogram bin width.

    Args:
        data:
            Numeric dataset.

        binwidth:
            Desired histogram bin width.

    Returns:
        np.ndarray:
            Histogram bin boundary array.

    Raises:
        ValueError:
            Raised when the provided bin width is invalid.
    """
    if binwidth <= 0:
        raise ValueError("binwidth must be a positive integer")
    return np.arange(
        data.min() // binwidth * binwidth,
        data.max() // binwidth * binwidth + binwidth + 1,
        binwidth,
    )


def calculate_weekly_ticks(dates: pd.Series) -> pd.DatetimeIndex:
    """
    Generate normalized weekly plotting ticks.

    The function expands the provided date range to complete calendar
    weeks and generates Monday-aligned plotting ticks.

    Args:
        dates:
            Pandas series containing datetime values.

    Returns:
        pd.DatetimeIndex:
            Weekly datetime tick positions.
    """
    min_date = dates.min().to_period("M").start_time
    ticks_start_date = min_date - pd.to_timedelta(min_date.weekday(), unit="D")

    max_date = dates.max().to_period("M").end_time
    ticks_end_date = max_date + pd.to_timedelta(6 - max_date.weekday(), unit="D")

    # Generate Monday-aligned weekly ticks.
    return pd.date_range(
        start=ticks_start_date, end=ticks_end_date, freq="W-MON"
    )  # freq="D")


def print_info() -> None:
    """
    Display rr2graph runtime environment information.

    The output includes:
        - rr2graph version
        - Python runtime version
        - installation location
        - current working directory
        - operating system information
        - terminal encoding
        - configuration file status

    Returns:
        None

    Examples:
        Display environment information:

            print_info()
    """

    print(f"{CYAN}rr2graph info{RESET}")
    print("──────────────────────────────────────────────")

    print(f"Version:        {__version__}")
    print(f"Python:         {platform.python_version()}")
    print(f"Installed in:   {os.path.dirname(pkg_file)}")
    print()

    # Current working directory.
    cwd = os.getcwd()
    print(f"Working dir:    {cwd}")

    # System information.
    print(
        f"System:         {platform.system()} "
        f"{platform.release()} ({platform.machine()})"
    )
    print(f"Terminal:       {sys.stdout.encoding}")
    print()

    # Inspect default configuration file.
    default_cfg = "config.yaml"
    if os.path.exists(default_cfg):
        print(f"{GREEN}Detected config file:{RESET} {default_cfg}")
        try:
            with open(default_cfg, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            excel = cfg.get("excel", "<not set>")
            months = cfg.get("num_of_months", "<not set>")
            output = cfg.get("output", "<not set>")
            print(f"  Excel file:      {excel}")
            print(f"  Months:          {months}")
            print(f"  Output directory:{output}")
        except Exception as e:
            print(f"{YELLOW}Warning: Failed to read config:{RESET} {e}")
    else:
        print(f"{YELLOW}No config file found " f"(config.yaml is missing).{RESET}")

    print("──────────────────────────────────────────────")
    print(f"{GREEN}Everything looks good ✓{RESET}")
