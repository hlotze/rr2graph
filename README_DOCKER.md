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

---

2. Testdaten erzeugen

    ```bash
    docker run --rm \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -g
    ```

    Dies erzeugt: `test_rr_data.xlsx`.

    Dabei bedeuten die Zeillen des Befehls:

    | Nr. | Zeile | Erklärung |
    | --- | --- | --- |
    | 1. | ```docker run --rm \``` | startet einen neuen Docker‑Container aus einem Image und löscht ihn nach Ausführung |
    | 2. | ```-v $(pwd):/data \``` | aktuelles Verzeichnis auf deinem Rechner wird auf den Zielpfad im Container gemapped |
    | 3. | ```-w /data \``` | setzt das working directory im Container. |
    | 4. | ```ghcr.io/hlotze/rr2graph:latest \``` | das Docker‑Image, das ausgeführt wird. |
    | 5. | ```-g``` | ```rr2graph -g``` : generate test_rr_data.xlsx |

    Ablauf des Docker Kommandos:

    1. Wenn das Docker-Image vorliegt (siehe Docker-Client >> Images) wird es genommen, sonst wird es erst heruntergeladen.
    2. Docker baut aus dem Image einen Container, dieser wird ausgeführt.
    3. Der Aufruf `docker run --rm \` löscht den Container gleich nach Ausführung, weil rr2graph ein CLI-tool ist. Es wird gestartet, produziert die Graphiken und beendet sich dann. Ohne `--rm` würde der Container inaktiv überleben, was bei Daemon (aka Hintergrund-) Prozessen nötig ist, nicht bei CLI-tools.

---

3. Plots aus den Testdaten erzeugen

    ```bash
    docker run --rm \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -e /data/test_rr_data.xlsx \
    -n 3 \
    -o /data/plots/test/
    ```

    Die erzeugten Diagramme finden Sie anschließend im Ordner: `plots/test/`

    Die Befehlszeilen bedeuten:

    | Nr. | Zeile | Erklärung |
    | --- | --- | --- |
    | 1. - 4. | | wie oben |
    | 5. | ```-e /data/test_rr_data.xlsx \``` | `test_rr_data.xlsx` aus dem Arbeitsverzeichnis |
    | 6. | ```-n 3 \``` | Daten der letzen 3 Monate sollen gezeigt werden. |
    | 7. | ```-o /data/plots/test/``` | Graphiken ins plots/test/ Verzeichnis des Arbeitsverzeichnis |  

    ---

    Sie können natürlich auch eigen eigene `rr_data.xlsx` nutzen, sofern sie die gleiche Struktur hat wie die `test_rr_data.xlsx` - nur mit Ihren Daten. Dann würde der Aufruf etwa so aussehen:

    ```bash
    docker run --rm \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -e /data/rr_data.xlsx \
    -n 3 \
    -o /data/plots
    ```

    Die Befehlszeilen bedeuten:

    | Nr. | Zeile | Erklärung |
    | --- | --- | --- |
    | 1. - 4. | | wie oben |
    | 5. | ```-e /data/rr_data.xlsx \``` | `rr_data.xlsx` aus dem Arbeitsverzeichnis |
    | 6. | ```-n 3 \``` | Daten der letzen 3 Monate sollen gezeigt werden. |
    | 7. | ```-o /data/plots``` | Graphiken ins plots/ Verzeichnis des Arbeitsverzeichnis |  

## ❓ Hilfe anzeigen

```bash
docker run --rm ghcr.io/hlotze/rr2graph:latest --help
```

Dies zeigt die vollständige Hilfe:

```text
usage: rr2graph [-h] [-e EXCEL] [-n NUM_OF_MONTHS] [-o OUTPUT] [-c CONFIG]
                [-v] [-g] [-i]

Liest Excel-Daten ein und erzeugt daraus Graphiken.

options:
  -h, --help            show this help message and exit
  -e EXCEL, --excel EXCEL
                        Pfad zur Excel-Datei (Default: rr_data.xlsx)
  -n NUM_OF_MONTHS, --num_of_months NUM_OF_MONTHS
                        Anzahl der Monate 1–6 (Default: 3)
  -o OUTPUT, --output OUTPUT
                        Output-Ordner für die erzeugten Plots (Default:
                        plots/)
  -c CONFIG, --config CONFIG
                        Pfad zu einer optionalen YAML-Konfigurationsdatei
  -v, --version         show program's version number and exit
  -g, --generate-test-data
                        Erzeugt test_rr_data.xlsx und beendet das Programm
  -i, --info            Zeigt System- und Konfigurationsinformationen an
```

## ℹ️ Informationen zur Installation

```bash
docker run --rm -v "$(pwd):/data" -w /data ghcr.io/hlotze/rr2graph:latest --info
```

liefert dann etwa:

```bash
rr2graph info
──────────────────────────────────────────────
Version:        0.2.2
Python:         3.11.15
Installiert in: /usr/local/lib/python3.11/site-packages/rr2graph

Arbeitsverz.:   /data
System:         Linux 6.10.14-linuxkit (aarch64)
Terminal:       utf-8

Gefundene Config-Datei: config.yaml
  Excel-Datei:   rr_data.xlsx
  Monate:        3
  Output-Ordner: plots/
──────────────────────────────────────────────
Alles sieht gut aus ✓
```

## 📦 Warum rr2graph bei jedem Aufruf einen neuen Docker‑Container startet

rr2graph wird als Command‑Line‑Tool ausgeführt:

Es liest Eingabedateien, erzeugt Ausgaben und beendet sich danach wieder.

Für solche Tools ist es Best Practice, bei jedem Aufruf einen neuen Container zu starten.

```bash
docker run --rm \
    -v $(pwd):/data \
    -w /data \
    ghcr.io/hlotze/rr2graph:latest \
    -e rr.xlsx -n 3
```

führt intern zwei Schritte aus:

1. Container erzeugen (einmalige Instanz des Images)
2. Container starten (führt das Tool aus)
   
Nach der Ausführung bleibt der Container als „exited“ liegen.

Beim nächsten Aufruf wird immer ein neuer Container erzeugt.

Das ist gewollt, denn Container sollen:
- kurzlebig sein
- keinen Zustand speichern
- jederzeit neu erzeugbar sein

und per `--rm` wird der nicht mehr benötigte Container, nach der Ausführung, gelöscht.


```text
                 +-----------------------------+
                 |     Docker Image Cache      |
                 |  ghcr.io/hlotze/rr2graph    |
                 +--------------+--------------+
                                |
                                |  (nur beim ersten Mal)
                                v
                     [Image wird lokal gespeichert]
                                |
                                v
+---------------------------------------------------------------+
|                       docker run ...                          |
+---------------------------------------------------------------+
                                |
                                v
                    +-----------------------+
                    |   Neuer Container     |
                    |   (ephemer / frisch)  |
                    +----------+------------+
                               |
                               |  Mount: -v $(pwd):/data
                               v
                +-----------------------------------+
                |   Host-Verzeichnis (persistente)   |
                |   ./rr.xlsx, ./config.yaml, ./out  |
                +-----------------------------------+
                               ^
                               |
                               |  Working Dir: -w /data
                               |
                    +----------+------------+
                    |   rr2graph CLI läuft  |
                    |   liest /data/*       |
                    |   schreibt /data/*    |
                    +----------+------------+
                               |
                               v
                    +-----------------------+
                    |   Container endet     |
                    |   (exit 0)            |
                    +----------+------------+
                               |
                               |  --rm (optional)
                               v
                    [Container wird gelöscht]
                               |
                               v
+---------------------------------------------------------------+
|       Daten bleiben im Host-Verzeichnis vollständig erhalten  |
+---------------------------------------------------------------+
```
