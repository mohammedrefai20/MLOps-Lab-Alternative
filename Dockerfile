FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy ONLY dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies — this layer gets CACHED after first run
RUN uv sync --frozen

# Copy the rest of the code AFTER installing
COPY app/ ./app/
COPY data/ ./data/
COPY main.py ./

EXPOSE 8000

CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]