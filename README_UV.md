# ⚡ rr2graph – Quickstart mit uv (End‑User)

Diese Anleitung richtet sich an Anwender, die rr2graph ohne venv oder pipenv, aber mit dem modernen Python‑Tool uv nutzen möchten.

uv bietet:

- extrem schnelle Installation
- automatische virtuelle Umgebungen
- pyproject‑basiertes Dependency‑Management
- keine Aktivierung von Umgebungen nötig
- reproduzierbare Builds

## ✅ Voraussetzungen

- Python 3.11 oder neuer
- uv installiert

Installation von uv:
  
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

oder unter macOS:

```bash
brew install uv
```

## 🚀 Quickstart (End‑User)

1. Neues Arbeitsverzeichnis anlegen

    ```bash
    mkdir rr2graph_test
    cd rr2graph_test
    ```

2. rr2graph installieren

    ```bash
    uv pip install rr2graph
    ```

3. Hilfe anzeigen

    ```bash
    uv run rr2graph -h
    ```

4. Installation prüfen

    ```bash
    uv run rr2graph --info
    ```

5. Testdaten erzeugen

    ```bash
    uv run rr2graph -g
    ```

    Dies erzeugt: `test_rr_data.xlsx`

6. Beispielplots erzeugen

    ```bash
    uv run rr2graph -e test_rr_data.xlsx -n 3
    ````

    Die erzeugten Diagramme finden Sie anschließend im Ordner: `plots/`

## 📘 Weitere Informationen

Für andere Installationsmethoden:

- Docker: README_DOCKER.md
- Python venv: README_VENV.md

# ⚡ rr2graph – Quickstart with uv (End User)

This guide is intended for users who want to run rr2graph without using venv or pipenv, but with the modern Python tool uv.

uv provides:

- extremely fast installation
- automatic virtual environments
- pyproject-based dependency management
- no need to manually activate environments
- reproducible builds

## ✅ Requirements

- Python 3.11 or newer
- uv installed

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or on macOS:

```bash
brew install uv
```

## 🚀 Quickstart (End User)

1. Create a new working directory

    ```bash
    mkdir rr2graph_test
    cd rr2graph_test
    ```

2. Install rr2graph

    ```bash
    uv pip install rr2graph
    ```

3. Show help

    ```bash
    uv run rr2graph -h
    ```

4. Verify installation

    ```bash
    uv run rr2graph --info
    ```

5. Generate test data

    ```bash
    uv run rr2graph -g
    ```

    This generates: `test_rr_data.xlsx`

6. Generate example plots

    ```bash
    uv run rr2graph -e test_rr_data.xlsx -n 3
    ```

    The generated plots can be found in the `plots/` directory.

## 📘 Further information

For other installation methods:

- Docker: README_DOCKER.md
- Python venv: README_VENV.md