# syntax=docker/dockerfile:1

FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

# Install the application dependencies.
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN --mount=from=ghcr.io/astral-sh/uv:0.11,source=/uv,target=/bin/uv \
    uv sync --frozen --no-cache --no-dev

# Copy the application into the container.
COPY app /app/app

# Run as a dedicated non-root user.
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --create-home app
USER app

EXPOSE 8000

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]
