FROM python:3.10-slim-bookworm

LABEL org.opencontainers.image.source="https://github.com/hlotze/rr2graph"
LABEL org.opencontainers.image.description="Heart rate variability analytics and visualization tool"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app

# Nur minimale Runtime-Abhängigkeiten
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 \
    libfreetype6 \
    libpng16-16 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zuerst nur Metadaten kopieren (besseres Docker-Caching)
COPY pyproject.toml .

# Projektcode kopieren
COPY rr2graph ./rr2graph

# Python-Pakete installieren
RUN pip install --no-cache-dir --no-compile .

# Zusätzlicher Cleanup
RUN find /usr/local/lib/python*/site-packages \
    -type d \( -name "tests" -o -name "test" -o -name "__pycache__" \) \
    -exec rm -rf {} + \
    && find /usr/local \
    -type f \( -name "*.pyc" -o -name "*.pyo" \) \
    -delete \
    && rm -rf /root/.cache \
    && rm -rf /tmp/*

ENTRYPOINT ["rr2graph"]
