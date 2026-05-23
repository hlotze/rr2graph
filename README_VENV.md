# 🐍 rr2graph – Quickstart (Virtual Environment, End User)

This guide is intended for users who want to run rr2graph locally with Python — without Docker, but inside a clean, isolated virtual environment using `venv`.

The following steps show how to test rr2graph in a fresh Python environment — exactly as a new user would do.

## ![GitHub Codespaces](examples/github_codspaces.svg) GitHub Codespaces

All steps are checked at Github Codespaces Terminal:

### 1. Create a new working directory

```bash
mkdir rr2graph_run
cd rr2graph_run
```

### 2. Create and activate a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install from PyPI

```bash
pip install rr2graph
```

### 4. Show help information

```bash
rr2graph -h
```

### 5. Verify the installation

```bash
rr2graph --info
```

### 6. Generate test data

```bash
rr2graph -g
```

This creates a file: `test_rr_data.xlsx`

### 7. Generate example plots

```bash
rr2graph -e test_rr_data.xlsx -n 3
```

The generated plots will appear in the directory: `plots/`

The Codespaces Terminal shows this:

```text
👋 Welcome to Codespaces! You are on our default image. 
   - It includes runtimes and tools for Python, Node.js, Docker, and more. See the full list here: https://aka.ms/ghcs-default-image
   - Want to use a custom image instead? Learn more here: https://aka.ms/configure-codespace

🔍 To explore VS Code to its fullest, search using the Command Palette (Cmd/Ctrl + Shift + P or F1).

📝 Edit away, run your app as usual, and we'll automatically make it available for you to access.

@<your username> ➜ /workspaces/codespaces-blank $ 

@<your username> ➜ /workspaces/codespaces-blank $ mkdir rr2graph_run
cd rr2graph_run


@<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ python -m venv venv
@<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ 

@<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ ls -a
.  ..  venv

@<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ source venv/bin/activate

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ pip install rr2graph
Collecting rr2graph
...
... installation process
...

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ rr2graph -h
usage: rr2graph [-h] [-e EXCEL] [-n NUM_OF_MONTHS] [-o OUTPUT] [-c CONFIG] [-v] [-g] [-i]

Load Excel datasets and generate RR visualization plots.

options:
  -h, --help            show this help message and exit
  -e EXCEL, --excel EXCEL
                        Path to the Excel input file (default: rr_data.xlsx)
  -n NUM_OF_MONTHS, --num_of_months NUM_OF_MONTHS
                        Number of months to visualize: 1-6 (default: 3)
  -o OUTPUT, --output OUTPUT
                        Output directory for generated plots (default: plots/)
  -c CONFIG, --config CONFIG
                        Path to an optional YAML configuration file
  -v, --version         show program's version number and exit
  -g, --generate-test-data
                        Generate test_rr_data.xlsx and exit the program
  -i, --info            Display runtime and configuration information

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ rr2graph --info
rr2graph info
──────────────────────────────────────────────
Version:        0.3.2
Python:         3.12.1
Installed in:   /workspaces/codespaces-blank/rr2graph_run/venv/lib/python3.12/site-packages/rr2graph

Working dir:    /workspaces/codespaces-blank/rr2graph_run
System:         Linux 6.8.0-1044-azure (x86_64)
Terminal:       utf-8

No config file found (config.yaml is missing).
──────────────────────────────────────────────
Everything looks good ✓

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ rr2graph -g
→ Generating test_rr_data.xlsx …
Finished! File created: test_rr_data.xlsx
         date  weight      time  rr_syst  rr_diast  heart_rate
0  23.11.2025    58.7  09:50:00      111        81          83
1  23.11.2025     NaN  08:50:00      117        78          85
2  24.11.2025    60.5  12:00:00      129        79          88
3  24.11.2025     NaN  09:40:00      112        81          72
4  24.11.2025     NaN  06:30:00      116        67          69
✓ Test dataset generated.

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ ls -a
.  ..  test_rr_data.xlsx  venv

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ rr2graph -e test_rr_data.xlsx -n 3
Heart rows read: 538
Weight rows read: 182

→ Excel file: test_rr_data.xlsx
→ Months: 3
→ Output directory: plots/

Generating histogram plots…
Generated histogram plots stored at:
-- plots/png/(2026-03__2026-05 3 months) per month data and histogram.png
-- plots/pdf/(2026-03__2026-05 3 months) per month data and histogram.pdf
-- plots/svg/(2026-03__2026-05 3 months) per month data and histogram.svg

Generating violin plots…
Generated violin plots stored at:
-- plots/png/(2026-03__2026-05 3 months) per month data and violin.png
-- plots/pdf/(2026-03__2026-05 3 months) per month data and violin.pdf
-- plots/svg/(2026-03__2026-05 3 months) per month data and violin.svg

Generating box_swarm plots…
Generated box_swarm plots stored at:
-- plots/png/(2026-03__2026-05 3 months) per month data and box_swarm.png
-- plots/pdf/(2026-03__2026-05 3 months) per month data and box_swarm.pdf
-- plots/svg/(2026-03__2026-05 3 months) per month data and box_swarm.svg

(venv) @<your username> ➜ /workspaces/codespaces-blank/rr2graph_run $ 
```
