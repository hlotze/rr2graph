FROM python:3.11-slim

# 1. Systemabhängigkeiten (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Arbeitsverzeichnis
WORKDIR /app

# 3. Projektdateien ins Image kopieren
COPY . /app

# 4. rr2graph installieren (PEP 517/518 build)
RUN pip install --no-cache-dir .

# 5. Standard-Datenverzeichnis im Container
#    (wird vom User per Volume überschrieben)
RUN mkdir -p /data

# 6. Entry Point: rr2graph CLI
ENTRYPOINT ["rr2graph"]
