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
curl -X POST "https://api.ecologits.ai/v1/estimations" \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai", "model": "gpt-4o-mini", "output_token_count":150, "request_latency":1.2}'
```

## Run API without Docker

- Install project's dependencies using uv (`uv sync`)
- Start the app using the following command: `uv run fastapi dev app/main.py`
- Check that the app is running on: [http://localhost:8000/docs](http://localhost:8000/docs)

## Run API with Docker

### Use published image

- Start container with: `docker run -p 8000:80 ghcr.io/mlco2/ecologits-api:latest`
- Check that the app is running on: [http://localhost:8000/docs](http://localhost:8000/docs)

### Build image yourself

- Build the Docker image with: `docker build -t ecologits-api .`
- Run the Docker container locally with: `docker run -p 8000:80 ecologits-api`
- Check that the app is running on: [http://localhost:8000/docs](http://localhost:8000/docs)

## Estimating environmental impacts

Use the `/estimations` endpoint to estimate the environmental impacts of your LLM generation requests by providing:

- Provider name (e.g., "openai")
- Model name (e.g., "gpt-4o-mini")
- Output token count
- Request latency
- Electricity mix zone (optional, defaults to "WOR")

Try it out at: [http://localhost:8000/docs#/default/post_estimations_v1_estimations_post](http://localhost:8000/docs#/default/post_estimations_v1_estimations_post)

## Run tests

- Install project's dependencies, including dev dependencies (`uv sync --group dev`)
- Run all tests using the following command: `uv run pytest`

## Resources

- [EcoLogits Documentation - Warnings and Errors](https://ecologits.ai/latest/tutorial/warnings_and_errors/) - Learn how to interpret warning and error values from the [models endpoint](http://localhost:8000/docs#/default/get_models_v1_models__providerName__get)
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
