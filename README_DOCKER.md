# 🐳 rr2graph – Docker Quickstart (End User)

This guide is intended for users who want to run rr2graph without installing Python locally — using only the official Docker container.

The container includes:

- the full rr2graph CLI
- all Python dependencies
- all plotting libraries
- multi-architecture support (AMD64 + ARM64)

This means rr2graph runs on:

- macOS (Intel & Apple Silicon)
- Windows
- Linux
- GitHub Codespaces
- any Docker-enabled system

![rr2graph at Docker Container](https://github.com/hlotze/rr2graph/blob/main/examples/rr2graph_at_container.png?raw=true)


## ✅ Requirements

To use rr2graph via Docker, you need:

1. Docker Desktop

   Available for:

   - macOS
   - Windows
   - Linux

   Download: https://www.docker.com/products/docker-desktop/

2. Internet connection

   The container image will be downloaded automatically from GitHub Container Registry (GHCR) on first run.

## 🚀 Quickstart (Docker)

The following steps show how to run rr2graph using Docker.

### 1. Create a working directory

```bash
mkdir rr2graph_run
cd rr2graph_run
```

---

### 2. Generate test data

```bash
docker run --rm \
  -v $(pwd):/data \
  -w /data \
  ghcr.io/hlotze/rr2graph:latest \
  -g
```

This generates: `test_rr_data.xlsx`.

Explanation of the command:

| Step | Command part | Explanation |
|------|-------------|-------------|
| 1 | `docker run --rm \` | starts a new Docker container from an image and removes it after execution |
| 2 | `-v $(pwd):/data \` | mounts the current host directory into the container at `/data` |
| 3 | `-w /data \` | sets the working directory inside the container |
| 4 | `ghcr.io/hlotze/rr2graph:latest \` | the Docker image to run |
| 5 | `-g` | `rr2graph -g`: generate test_rr_data.xlsx |

How Docker executes this command:

1. If the image is not available locally, it is downloaded first.
2. Docker creates a container from the image.
3. The container runs the rr2graph CLI.
4. The `--rm` flag ensures the container is removed after execution.

---

### 3. Generate plots from test data

```bash
docker run --rm \
  -v $(pwd):/data \
  -w /data \
  ghcr.io/hlotze/rr2graph:latest \
  -e /data/test_rr_data.xlsx \
  -n 3 \
  -o /data/plots/test/
```

The generated plots can be found in: `plots/test/`

Explanation of the command:

| Step | Command part | Explanation |
|------|-------------|-------------|
| 1–4 | as above | base Docker setup |
| 5 | `-e /data/test_rr_data.xlsx \` | input Excel file |
| 6 | `-n 3 \` | number of months to display |
| 7 | `-o /data/plots/test/` | output directory for generated plots |

---

You can also use your own `rr_data.xlsx`, as long as it matches the expected structure of `test_rr_data.xlsx`.

Example:

```bash
docker run --rm \
  -v $(pwd):/data \
  -w /data \
  ghcr.io/hlotze/rr2graph:latest \
  -e /data/rr_data.xlsx \
  -n 3 \
  -o /data/plots
```

Explanation:

| Step | Command part | Explanation |
|------|-------------|-------------|
| 1–4 | as above | base Docker setup |
| 5 | `-e /data/rr_data.xlsx \` | user-provided Excel file |
| 6 | `-n 3 \` | number of months to display |
| 7 | `-o /data/plots` | output directory |

## ❓ Help

```bash
docker run --rm ghcr.io/hlotze/rr2graph:latest --help
```

This shows the full CLI help:

```text
usage: rr2graph [-h] [-e EXCEL] [-n NUM_OF_MONTHS] [-o OUTPUT] [-c CONFIG]
                [-v] [-g] [-i]

Reads Excel data and generates plots.

options:
  -h, --help            show this help message and exit
  -e EXCEL, --excel EXCEL
                        Path to Excel file (default: rr_data.xlsx)
  -n NUM_OF_MONTHS, --num_of_months NUM_OF_MONTHS
                        Number of months 1–6 (default: 3)
  -o OUTPUT, --output OUTPUT
                        Output directory for generated plots (default:
                        plots/)
  -c CONFIG, --config CONFIG
                        Path to optional YAML configuration file
  -v, --version         show program version and exit
  -g, --generate-test-data
                        Generates test_rr_data.xlsx and exits
  -i, --info           Show system and configuration information
```

## ℹ️ Installation information

```bash
docker run --rm -v "$(pwd):/data" -w /data ghcr.io/hlotze/rr2graph:latest --info
```

Example output:

```text
rr2graph info
──────────────────────────────────────────────
Version:        0.2.2
Python:         3.11.15
Installed in:   /usr/local/lib/python3.11/site-packages/rr2graph

Working dir:    /data
System:         Linux 6.10.14-linuxkit (aarch64)
Terminal:       utf-8

Detected config file: config.yaml
  Excel file:   rr_data.xlsx
  Months:       3
  Output dir:   plots/
──────────────────────────────────────────────
Everything looks good ✓
```

## 📦 Why rr2graph creates a new Docker container on each run

rr2graph is a command-line tool:

It reads input files, generates output, and then exits.

For this type of tool, it is best practice to start a fresh container on each run.

```bash
docker run --rm \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -e rr.xlsx -n 3
```

Internally, Docker performs two steps:

1. Create a container from the image
2. Run the container

After execution, the container stops.

With `--rm`, it is automatically removed afterwards.

This is intentional because containers should:

- be stateless
- be reproducible
- be disposable
