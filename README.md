# Ecologits API

An API to estimate the environmental impacts of LLM generation requests.

## Start the app

- Install project's dependencies using uv (`uv sync`)
- Start the app using the following command: `uv run fastapi dev app/main.py`
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
