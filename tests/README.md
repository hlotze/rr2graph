# Tests für rr2graph

Dieses Verzeichnis enthält die komplette pytest‑Suite für das Projekt **rr2graph**.  
Die Tests decken alle Module ab:

- `io.py` – Einlesen und Parsen der Excel‑Daten  
- `helpers.py` – Hilfsfunktionen (valid_month, ticks, bins, config)  
- `layout.py` – Erzeugung der Figure‑Layouts  
- `monthly.py` – Monatslogik und Orchestrierung der Plot‑Zeilen  
- `orchestrator.py` – Speichern der Plots in PNG/PDF/SVG  
- `plots/*` – Scatter, Histogramm, Violin, Box‑Swarm  
- `cli.py` – Kommandozeilen‑Interface  

## Struktur

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

## Tests ausführen

Im Projekt‑Root:

```python
pytest
```

Oder mit ausführlicher Ausgabe:

```python
pytest -v
```

oder mit ruff

```python
pipenv run ruff check rr2graph
pipenv run ruff check tests/
````

## Coverage

Falls `pytest.ini` Coverage aktiviert:

```python
pytest –cov
````

HTML‑Report:

```python
pytest –cov –cov-report=html
open htmlcov/index.html
```

## Hinweise

- Die Plot‑Tests verwenden das Matplotlib‑Backend **Agg**, damit keine GUI geöffnet wird.
- Die IO‑Tests erzeugen temporäre Excel‑Dateien im `tmp_path`‑Fixture.
- Die CLI‑Tests mocken alle externen Funktionen, damit keine echten Plots oder Dateien erzeugt werden.
- Die Tests sind so geschrieben, dass sie unabhängig von Betriebssystem, Pfaden und Zeitzonen laufen.

Viel Spaß beim Testen!
