sync-dev:
	uv sync --group dev

start:
	uv run fastapi dev app/main.py

build-docker:
	docker build -t ecologits-api .

run-docker:
	docker run -p 8000:80 ecologits-api

test:
	uv run pytest

format:
	uv run ruff check --select I --fix && uv run ruff format

check-fix:
	uv run ruff check --fix && uv run ruff check --select I --fix