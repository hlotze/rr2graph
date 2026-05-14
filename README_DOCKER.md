# 🐳 rr2graph – Docker Quickstart (End‑User)

Diese Anleitung richtet sich an Anwender, die rr2graph ohne lokale Python‑Installation nutzen möchten — ausschließlich über den offiziellen Docker‑Container.

Der Container enthält:

- die vollständige rr2graph‑CLI
- alle Python‑Abhängigkeiten
- alle Plot‑Bibliotheken
- Multi‑Arch‑Support (AMD64 + ARM64)

Damit läuft rr2graph auf:

- macOS (Intel & Apple Silicon)
- Windows
- Linux
- GitHub Codespaces
- jedem Docker‑fähigen System

## ✅ Voraussetzungen

Um rr2graph per Docker zu nutzen, benötigen Sie:

1. Docker Desktop

    Installierbar für:

    - macOS
    - Windows
    - Linux

    Download: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

2. Internetverbindung

    Der Container wird beim ersten Start automatisch aus der GitHub Container Registry (GHCR) geladen.

## 🚀 Quickstart (Docker)

Die folgenden Schritte zeigen, wie Sie rr2graph mit Docker ausführen.

1. Arbeitsverzeichnis anlegen

    ```bash
    mkdir rr2graph_run
    cd rr2graph_run
    ```

2. Testdaten erzeugen

    ```bash
    docker run \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -g
    ```

    Dies erzeugt: `test_rr_data.xlsx`

3. Plots aus den Testdaten erzeugen

    ```bash
    docker run \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -e /data/test_rr_data.xlsx \
    -n 3 \
    -o /data/plots
    ```

    Die erzeugten Diagramme finden Sie anschließend im Ordner: `plots/`

    Sie können natürlich auch eigen eigene `rr_data.xlsx` nutzen, sofern sie die gleiche Struktur hat wie die `test_rr_data.xlsx` - nur mit Ihren Daten. Dann würde der Aufruf etwa so aussehen:

    ```bash
        docker run \
        -v $(pwd):/data \
        -w /data \
        ghcr.io/hlotze/rr2graph:latest \
        -e /data/rr_data.xlsx \
        -n 3 \
        -o /data/plot
    ```

## ❓ Hilfe anzeigen

```bash
docker run ghcr.io/hlotze/rr2graph:latest --help
```

Dies zeigt die vollständige Hilfe:

```text
Usage: rr2graph [OPTIONS]

Options:
  -e, --excel PATH         Pfad zur Excel-Datei mit den Rohdaten
  -n, --months INTEGER     Anzahl der Monate, die ausgewertet werden sollen
  -o, --output PATH        Ausgabeordner für die erzeugten Plots
  -g, --generate           Erzeugt eine Beispiel-Excel-Datei (test_rr_data.xlsx)
  --info                   Zeigt Informationen zur Installation und Version
  -h, --help               Zeigt diese Hilfe an und beendet das Programm
```

## ℹ️ Informationen zur Installation

```bash
docker run ghcr.io/hlotze/rr2graph:latest --info
```
