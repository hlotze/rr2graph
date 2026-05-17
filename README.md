# 📘 rr2graph — Visualize Blood Pressure, Pulse, and Weight Data

[![PyPI Version](https://img.shields.io/pypi/v/rr2graph)](https://pypi.org/project/rr2graph/)
![Python Versions](https://img.shields.io/pypi/pyversions/rr2graph)
![Downloads](https://img.shields.io/pypi/dm/rr2graph)

![CI Status](https://github.com/hlotze/rr2graph/actions/workflows/python-ci.yml/badge.svg)
[![Coverage](https://codecov.io/gh/hlotze/rr2graph/branch/main/graph/badge.svg)](https://codecov.io/gh/hlotze/rr2graph)

![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/hlotze/rr2graph)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

[![GHCR](https://img.shields.io/badge/GHCR-rr2graph-blue?logo=github)](https://github.com/hlotze/rr2graph/pkgs/container/rr2graph)
![Docker Pulls](https://img.shields.io/badge/GHCR%20Pulls-Automatic-blue?logo=docker)
![Docker Image](https://img.shields.io/badge/Multi--Arch-AMD64%20%7C%20ARM64-green?logo=docker)

`rr2graph` is a lightweight command‑line tool for processing and visualizing blood pressure, pulse, and weight data stored in Excel files.  
It generates monthly plots (box‑swarm, scatter, histogram, violin) and exports them automatically as PNG, PDF, and SVG.

## 📤 Example Output

Example visualization using scatter and box‑swarm plots:

![Example Box Swarm Plot](https://github.com/hlotze/rr2graph/blob/main/examples/example_box_swarm.png?raw=true)

Format: **A4 Landscape (11.69 × 8.27 inch)**

The CLI prints all generated files:

```text
Heart rows read: 81
Weight rows read: 49
→ Excel file: rr_data.xlsx
→ Months: 3
→ Output folder: plots/
Generating histogram plots…
Generated histogram plots stored at:
– plots/png/(2026-02__2026-04 3 months) per month data and histogram.png
– plots/pdf/(2026-02__2026-04 3 months) per month data and histogram.pdf
– plots/svg/(2026-02__2026-04 3 months) per month data and histogram.svg
…
```

## 🐳 Docker Quickstart (End‑User)

🇩🇪 Wenn Sie rr2graph ohne lokale Python‑Installation nutzen möchten,
finden Sie eine vollständige Anleitung in:

👉 [Docker - Quickstart für End‑User](./README_DOCKER.md)

## 🐍 Python Quickstart (Virtual Environment, End‑User)

🇩🇪 Wenn Sie rr2graph lokal mit Python in einer isolierten Umgebung nutzen möchten, finden Sie eine vollständige Schritt‑für‑Schritt‑Anleitung in:

👉 [.venv - Quickstart (Virtual Environment, End‑User)](./README_VENV.md)

## ⚡ Python Quickstart mit uv (End‑User)

Für Nutzer, die rr2graph mit dem modernen Python‑Tool uv verwenden möchten:

👉 [Quickstart mit uv (End‑User)](./README_UV.md)

## 🚀 Installation

As I'm working with `pipenv`, the rest of the documentation is for `pipenv` users:

1. Ensure you are in the project root

    > ~/your/project/directory/

2. Install using Pipenv (editable mode)

    ```bash
    pipenv install -e .
    ```

    This installs:
    - the rr2graph package (editable mode)
    - all dependencies defined in pyproject.toml

3. Optional: Development dependencies

    ```bash
    pipenv install -r requirements_dev.txt
    ```

## 🧰 CLI Usage

After installation, the command rr2graph becomes available.

Show help

```bash
rr2graph --help
```

```text
usage: rr2graph [-h] [-e EXCEL] [-n NUM_OF_MONTHS] [-o OUTPUT] [-c CONFIG] [-v] [-g] [-i]

Reads Excel data and generates plots.

options:
  -h, --help            Show help and exit
  -e, --excel EXCEL     Path to Excel file (default: rr_data.xlsx)
  -n, --num_of_months NUM_OF_MONTHS
                        Number of months 1–6 (default: 3)
  -o, --output OUTPUT   Output folder for generated plots (default: plots/)
  -c, --config CONFIG   Optional YAML configuration file
  -v, --version         Show program version and exit
  -g, --generate-test-data
                        Generate test_rr_data.xlsx and exit
  -i, --info            Show system and configuration information
```

## 🧪 Generate Test Data

```bash
rr2graph -g
```

Creates:

> test_rr_data.xlsx

with realistic blood pressure, pulse, and weight data.

## ℹ️ System & Configuration Info

```bash
rr2graph --info
```

Example output:

```text
rr2graph info
──────────────────────────────────────────────
Version:        1.1.0
Python:         3.11.15
Installed at:   /opt/homebrew/lib/python3.11/site-packages/rr2graph

Working dir:    /Users/your_user/rr2graph_test
System:         Darwin 25.3.0 (arm64)
Terminal:       utf-8

No config file found (config.yaml missing).
──────────────────────────────────────────────
Everything looks good ✓
```

## 📝 Configuration File (YAML)

Example config.yaml:

```python
excel: "rr_data.xlsx"
num_of_months: 3
output: "plots/"
```

| Field | Description |
| ----- | ----- |
| excel | Path to the Excel file containing RR data |
| num_of_months | Number of months to analyze |
| output | Output directory for PNG/PDF/SVG plots |

Use it via:

```bash
rr2graph -c config.yaml
```

## 📊 Output Structure

Running:

```bash
rr2graph -c config.yaml
```

produces:

```text
plots/
├── png/
├── pdf/
└── svg/
```

## 📁 Project Structure

```text
/your/project/directory/
.
├── config.yaml
├── examples/example_box_swarm.png
├── Pipfile
├── plots/
│   ├── pdf/
│   ├── png/
│   ├── svg/
│   └── test/
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements_dev.txt
├── rr_data.xlsx
├── rr2graph/
│   ├── cli.py
│   ├── helpers.py
│   ├── io.py
│   ├── layout.py
│   ├── monthly.py
│   ├── orchestrator.py
│   ├── tools/
│   │   └── bump_version.py
│   └── plots/
│       ├── box_swarm.py
│       ├── hist.py
│       ├── scatter.py
│       └── violin.py
├── test_config.yaml
├── test_rr_data.xlsx
└── tests/
    └── test_rr2graph.py
```

## 🧪 Run Tests

```bash
pipenv run pytest
```

## 🛠 Troubleshooting

❌ UnicodeDecodeError in YAML

You likely passed an Excel file as --config.

Correct:

```bash
rr2graph -c config.yaml
```

Incorrect:

```bash
rr2graph -c test_rr_data.xlsx
```

❌ CLI command not found

Reinstall:

```bash
pipenv install -e .
```

## 👨‍💻 Developer Notes

Version bumping is handled via:

```text
make version-patch
make version-minor
make version-major
```

TestPyPI upload:

```bash
make publish-test
```

Build artifacts:

```text
make build
```

Manpage installation:

```text
make install-man
make man
```

## 📄 License

MIT
