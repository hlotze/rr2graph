"""provides several helper functions"""

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
BLUE = "\033[94m"
MAGENTA = "\033[95m"


def valid_month(value):
    """check given num_of_month value (1..6)"""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Monate müssen eine Zahl sein (1–6).")
    if ivalue < 1 or ivalue > 6:
        raise argparse.ArgumentTypeError("Monate müssen zwischen 1 und 6 liegen.")
    return ivalue


def load_config(path):
    """loads the yaml config file"""
    if path is None:
        return {}
    if not os.path.exists(path):
        print(f"[WARN] Config-Datei nicht gefunden: {path} – ignoriere sie.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def ensure_output_dirs(base: str) -> None:
    """ensures existance of output directories"""
    subdirs = ["png", "pdf", "svg"]
    os.makedirs(base, exist_ok=True)
    for sd in subdirs:
        os.makedirs(os.path.join(base, sd), exist_ok=True)


def binwidth_2_bins(data: np.ndarray, binwidth: int) -> np.ndarray:
    """calculates the bin array for a given bin width"""
    if binwidth <= 0:
        raise ValueError("binwidth must be a positive integer")
    return np.arange(
        data.min() // binwidth * binwidth,
        data.max() // binwidth * binwidth + binwidth + 1,
        binwidth,
    )


def calculate_weekly_ticks(dates: pd.Series) -> pd.DatetimeIndex:
    """generates the ticks array"""
    min_date = dates.min().to_period("M").start_time
    ticks_start_date = min_date - pd.to_timedelta(min_date.weekday(), unit="D")

    max_date = dates.max().to_period("M").end_time
    ticks_end_date = max_date + pd.to_timedelta(6 - max_date.weekday(), unit="D")

    # jetzt: tägliche Ticks
    return pd.date_range(
        start=ticks_start_date, end=ticks_end_date, freq="W-MON"
    )  # freq="D")


def print_info():
    """provides environment information"""

    print(f"{CYAN}rr2graph info{RESET}")
    print("──────────────────────────────────────────────")

    print(f"Version:        {__version__}")
    print(f"Python:         {platform.python_version()}")
    print(f"Installiert in: {os.path.dirname(pkg_file)}")
    print()

    # Arbeitsverzeichnis
    cwd = os.getcwd()
    print(f"Arbeitsverz.:   {cwd}")

    # Systeminfo
    print(
        f"System:         {platform.system()} "
        f"{platform.release()} ({platform.machine()})"
    )
    print(f"Terminal:       {sys.stdout.encoding}")
    print()

    # Config prüfen
    default_cfg = "config.yaml"
    if os.path.exists(default_cfg):
        print(f"{GREEN}Gefundene Config-Datei:{RESET} {default_cfg}")
        try:
            with open(default_cfg, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            excel = cfg.get("excel", "<nicht gesetzt>")
            months = cfg.get("num_of_months", "<nicht gesetzt>")
            output = cfg.get("output", "<nicht gesetzt>")
            print(f"  Excel-Datei:   {excel}")
            print(f"  Monate:        {months}")
            print(f"  Output-Ordner: {output}")
        except Exception as e:
            print(
                f"{YELLOW}Warnung: " f"Config konnte nicht gelesen werden:{RESET} {e}"
            )
    else:
        print(f"{YELLOW}Keine Config-Datei gefunden " f"(config.yaml fehlt).{RESET}")

    print("──────────────────────────────────────────────")
    print(f"{GREEN}Alles sieht gut aus ✓{RESET}")
