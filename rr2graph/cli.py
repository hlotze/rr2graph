"""collection of functions needed at command line"""

import argparse
from . import VERSION, XLSX_FN, NUM_OF_MONTHS, OUTPUT_DIR
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


def parse_args():
    """parse the given commandline arguments"""
    parser = argparse.ArgumentParser(
        description="Liest Excel-Daten ein und erzeugt daraus Graphiken."
    )

    parser.add_argument(
        "-e",
        "--excel",
        type=str,
        default=None,
        help=f"Pfad zur Excel-Datei (Default: {XLSX_FN})",
    )

    parser.add_argument(
        "-n",
        "--num_of_months",
        type=valid_month,
        default=None,
        help=f"Anzahl der Monate 1–6 (Default: {NUM_OF_MONTHS})",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help=f"Output-Ordner für die erzeugten Plots (Default: {OUTPUT_DIR})",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Pfad zu einer optionalen YAML-Konfigurationsdatei",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"rr2graph {VERSION}"
    )

    parser.add_argument(
        "-g",
        "--generate-test-data",
        action="store_true",
        help="Erzeugt test_rr_data.xlsx und beendet das Programm",
    )

    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Zeigt System- und Konfigurationsinformationen an",
    )
    return parser.parse_args()


def main():
    """main entrypoint to rr2graph"""
    args = parse_args()

    if args.info:
        print_info()
        return

    if args.generate_test_data:
        print("→ Generiere test_rr_data.xlsx …")
        generate_test_data_xlsx()
        print("✓ Testdaten erzeugt.")
        return

    cfg = load_config(args.config)

    excel_fn = args.excel or cfg.get("excel", XLSX_FN)
    num_months = args.num_of_months or cfg.get("num_of_months", NUM_OF_MONTHS)
    out_dir = args.output or cfg.get("output", OUTPUT_DIR)

    df_heart = read_heart_data(excel_fn)
    df_weight = read_weight_data(excel_fn)

    print("Heart rows read:", len(df_heart))
    print("Weight rows read:", len(df_weight))
    print()

    print(f"{CYAN}→ Excel-Datei:{RESET} {excel_fn}")
    print(f"{CYAN}→ Monate:{RESET} {num_months}")
    print(f"{CYAN}→ Output-Ordner:{RESET} {out_dir}")
    print()

    plot_types = ("histogram", "violin", "box_swarm")

    for plot_type in plot_types:
        print(f"{YELLOW}Generating {plot_type} plots…{RESET}")
        files = generate_monthly_plots(
            plot_type, num_months, df_heart, df_weight, out_dir
        )

        print(f"{GREEN}Generated {plot_type} plots stored at:{RESET}")
        for f in files:
            print(f"{BLUE}-- {f}{RESET}")
        print()


if __name__ == "__main__":
    main()
