FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

# Install the application dependencies.
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-cache

# Copy the application into the container.
COPY . /app

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
