# Ecologits API

An API to estimate the environmental impacts of LLM generation requests.

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

- Install project's dependencies including dev dependencies (`uv sync --group dev`)
- Run all tests using the following command: `uv run pytest`

## Resources

- [EcoLogits Documentation - Warnings and Errors](https://ecologits.ai/latest/tutorial/warnings_and_errors/) - Learn how to interpret warning and error values from the [models endpoint](http://localhost:8000/docs#/default/get_models_v1_models__providerName__get)
- [EcoLogits Documentation - Electricity Mix](https://ecologits.ai/latest/tutorial/impacts/#electricity-mix) - Learn how to choose the appropriate electricity mix zone for your calculations
