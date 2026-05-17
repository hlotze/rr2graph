FROM python:3.11-slim-bookworm

WORKDIR /app

# Install runtime dependencies for numpy/pandas/matplotlib wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 \
    libfreetype6 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copy project
COPY pyproject.toml .
COPY rr2graph ./rr2graph

# Install dependencies directly (NO wheel building!)
RUN pip install --no-cache-dir .

ENTRYPOINT ["rr2graph"]
