# Tests for rr2graph

This directory contains the complete pytest suite for the **rr2graph** project.  
The tests cover all major modules:

- `io.py` – Reading and parsing Excel data  
- `helpers.py` – Helper utilities (valid_month, ticks, bins, config)  
- `layout.py` – Figure layout generation  
- `monthly.py` – Monthly orchestration and plot row handling  
- `orchestrator.py` – Saving plots as PNG/PDF/SVG  
- `plots/*` – Scatter, histogram, violin, and box-swarm plots  
- `cli.py` – Command-line interface  

## Structure

```code
tests/
│
├── conftest.py
├── test_cli.py
├── test_helpers.py
├── test_io.py
├── test_layout.py
├── test_monthly.py
└── test_plots.py
```

## Running the tests

From the project root:

```python
pytest
```

Or with verbose output:

```python
pytest -v
```

Or run Ruff linting:

```python
pipenv run ruff check rr2graph
pipenv run ruff check tests/
````

## Coverage

If coverage is enabled in `pytest.ini`:

```python
pytest –cov
````

HTML report:

```python
pytest –cov –cov-report=html
open htmlcov/index.html
```

## Notes

- Plot tests use the Matplotlib **Agg** backend so no GUI windows are opened.
- IO tests generate temporary Excel files using the `tmp_path` fixture.
- CLI tests mock external functions to avoid generating real plots or files.
- The test suite is designed to run independently of operating systems, filesystem paths, and time zones.

Happy testing!
