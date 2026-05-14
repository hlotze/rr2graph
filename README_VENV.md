# 🐍 rr2graph – Quickstart (Virtual Environment, End‑User)

🇩🇪 Diese Anleitung richtet sich an Anwender, die rr2graph lokal mit Python nutzen möchten — ohne Docker, aber in einer sauberen, isolierten Python‑Umgebung.

The following steps show how to test rr2graph in a clean Python environment — exactly as a new user would do.

1. Create a new working directory

    ```bash
    mkdir rr2graph_run
    cd rr2graph_run
    ```

2. Create and activate a virtual environment

    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3. Install from PyPI

    ```bash
    pip install rr2graph
    ```

4. see the help information

    ```bash
    rr2graph -h
    ```

5. Verify the installation

    ```bash
    rr2graph --info
    ```

6. Generate test data

    ```bash
    rr2graph -g
    ```

    This creates a file: `test_rr_data.xlsx`

7. Generate example plots

    ```bash
    rr2graph -e test_rr_data.xlsx -n 3
    ```

    The generated plots will appear in the directory: `plots/`
