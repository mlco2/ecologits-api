<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/logo_dark.png">
    <img alt="EcoLogits" src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/logo_light.png" width="280">
  </picture>
</p>

# Ecologits API

An API to estimate the environmental impacts of LLM generation requests.

Part of [EcoLogits](https://github.com/mlco2/ecologits), maintained by the [Code Carbon](https://www.helloasso.com/associations/code-carbon) non-profit. **Live docs:** [api.ecologits.ai/docs](https://api.ecologits.ai/docs)

> **Local compute?** See [CodeCarbon](https://github.com/mlco2/codecarbon). **GenAI API calls?** Use `pip install ecologits` instead.

## Quick try

```bash
curl -X POST "https://api.ecologits.ai/v1beta/estimations" \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai", "model_name": "gpt-4o-mini", "output_token_count":150, "request_latency":1.2}'
```

The API uses EcoLogits `0.11.3` and exposes estimation and catalog routes under `/v1beta`. Use `GET /health` for a lightweight health check; it returns HTTP `200` with `{"status":"ok"}` when the API is running.

## Run API without Docker

Requires Python 3.11 or newer.

- Install the project's locked dependencies using uv (`uv sync --locked --no-dev`)
- Start the app using the following command: `uv run --locked --no-dev fastapi dev app/main.py`
- Check that the app is running on: [http://localhost:8000/docs](http://localhost:8000/docs)

## Run API with Docker

The image runs as a non-root user (UID/GID `10001`) and listens on `0.0.0.0:8000`. Python logs are unbuffered. It includes application code and runtime dependencies; uv, Ruff, pytest, and local `.env` files are excluded. Pass configuration with Docker's `-e` or `--env-file` options.

### Use published image

- Start container with: `docker run -p 8000:8000 ghcr.io/mlco2/ecologits-api:latest`
- Check that the app is running on: [http://localhost:8000/docs](http://localhost:8000/docs)

The published `latest` tag is updated after the release workflow succeeds. Use a specific release tag or digest for production.

### Build image yourself

- Use Docker with BuildKit support; the build temporarily mounts uv to install dependencies.
- Build the Docker image with: `docker build -t ecologits-api .`
- Run the Docker container locally with: `docker run -p 8000:8000 ecologits-api`
- Check that the app is running on: [http://localhost:8000/docs](http://localhost:8000/docs)

## Health checks

```bash
curl --fail http://localhost:8000/health
```

Expect HTTP `200` with `{"status":"ok"}`. This unversioned endpoint confirms the API is responding without running an estimation or calling external services. Configure your platform's HTTP probe to use `/health` on container port `8000`.

## Deploy on your own infrastructure

See the [deployment guide](DEPLOYMENT.md) for a simple guide to running the API on your company’s infrastructure.

## Estimating environmental impacts

Use the `/v1beta/estimations` endpoint to estimate the environmental impacts of your LLM generation requests by providing:

- Provider name (e.g., "openai")
- Model name (e.g., "gpt-4o-mini")
- Output token count
- Request latency (optional)
- Electricity mix zone (optional, defaults to "WOR")

Try it out at: [http://localhost:8000/docs#/Estimations/post_estimations_v1beta_estimations_post](http://localhost:8000/docs#/Estimations/post_estimations_v1beta_estimations_post)

## Run tests

- Install the project's locked dependencies, including Ruff and pytest: `uv sync --locked --group dev`.
- Run all tests: `uv run --locked --no-sync pytest`.
- Check a locally built Docker image: `bash .github/scripts/check-container.sh ecologits-api`.

CI runs the tests on Python 3.11 and 3.13, lints the Dockerfile with Hadolint, and builds and checks the production container on pull requests and pushes to `main`. Release tags run the same checks before publishing images for `linux/amd64` and `linux/arm64`. Clever Cloud deployment follows successful checks on `main`.

## Resources

- [EcoLogits Documentation - Warnings and Errors](https://ecologits.ai/latest/tutorial/warnings_and_errors/) - Learn how to interpret warning and error values from the [models endpoint](http://localhost:8000/docs#/Catalog/get_models_v1beta_models__provider_name__get)
- [EcoLogits Documentation - Electricity Mix](https://ecologits.ai/latest/tutorial/impacts/#electricity-mix) - Learn how to choose the appropriate electricity mix zone for your calculations
- [EcoLogits Python library](https://github.com/mlco2/ecologits) · [Calculator](https://calculator.ecologits.ai/) · [mlco2 organisation](https://github.com/mlco2)
- Community integrations using this API: [ecologits-statusline](https://github.com/DuarteVi/ecologits-statusline) · [ecologits-vscode](https://github.com/marmelab/ecologits-vscode)

## Sponsors

EcoLogits is supported by volunteers and:

<a href="https://resilio-solutions.com/" target="_blank">
<img src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/sponsors/resilio.png" alt="Resilio" height="60" width="150">
</a>
<a href="https://www.terra-cognita.ai/" target="_blank">
<img src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/sponsors/terra_cognita.png" alt="Terra Cognita" height="60" width="150">
</a>
<a href="https://sopht.com/" target="_blank">
<img src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/sponsors/sopht.png" alt="Sopht" height="60" width="150">
</a>
<a href="https://www.avanade.com/" target="_blank">
<img src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/sponsors/avanade.png" alt="Avanade" height="60" width="150">
</a>
<a href="https://www.theodo.com/" target="_blank">
<img src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/sponsors/theodo.png" alt="Theodo" height="60" width="150">
</a>
<a href="https://www.culture.gouv.fr/" target="_blank">
<img src="https://raw.githubusercontent.com/mlco2/ecologits/main/docs/assets/sponsors/ministere_culture.png" alt="Ministère de la Culture" height="60" width="80">
</a>
