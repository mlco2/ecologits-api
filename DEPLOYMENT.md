# Deploy EcoLogits API on your own infrastructure

EcoLogits API can run on a company VM, a managed container platform, or Kubernetes. The easiest approach is to deploy its Docker image behind your existing company gateway or reverse proxy.

## What you need

- A container runtime. No GPU is required.
- No database or persistent storage.
- No LLM provider API keys. The API calculates estimates locally using data bundled with EcoLogits.
- An optional gateway or reverse proxy to provide HTTPS and control access.

## 1. Run the API

On a machine with Docker installed:

```bash
docker run -d \
  --name ecologits-api \
  --restart unless-stopped \
  -p 127.0.0.1:8000:8000 \
  ghcr.io/mlco2/ecologits-api:latest
```

The API is now available at `http://127.0.0.1:8000`, with interactive documentation at `http://127.0.0.1:8000/docs`. The example binds to localhost so a reverse proxy on the same machine can forward requests to it.

Use a specific release tag or image digest instead of `latest` for production so deployments use a known version. You can also mirror the image into your company's registry.

Optional: if a browser frontend calls the API from a different origin, set `ALLOWED_ORIGINS` to its origin, for example by adding `-e 'ALLOWED_ORIGINS=["https://portal.example.com"]'` before the image name. This is unnecessary for backend-to-backend calls. The default is `["*"]`; setting explicit origins restricts browser access, but does not authenticate callers. CORS values must be JSON arrays.

### Build your own image instead

From a clean checkout of your chosen revision, use Docker with BuildKit support. The build temporarily mounts uv to install the locked runtime dependencies:

```bash
docker build -t ecologits-api .
```

Use `ecologits-api` in place of the published image in the run command. The Dockerfile copies only the application and dependency manifests into the image. Local `.env` files are excluded from the build context; pass configuration through environment variables at runtime.

## 2. Connect it to your infrastructure

For a managed container service or Kubernetes, use the same image with these settings:

| Setting | Value |
| --- | --- |
| Container port | `8000`, HTTP |
| Runtime user | Non-root, UID/GID `10001` |
| Startup command | Use the image's default command. |
| Health check | `GET /health`, expecting HTTP `200` and `{"status":"ok"}` |
| Environment | Set `ALLOWED_ORIGINS` if a browser frontend calls the API. |
| Persistent storage | None |

Configure HTTP health probes in your platform or monitoring system using `/health`. The route is unversioned and confirms that the API is responding. The image does not define a Docker `HEALTHCHECK` instruction.

If your platform requires a different port, override the startup command and update the target port and health check accordingly. For example, to listen on port `8080`:

```bash
/app/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
```

The default command does not automatically read a platform's `PORT` environment variable.

Point your gateway or reverse proxy to the API and give it a company URL, such as `https://ecologits-api.example.com`. For Docker on a VM, the example uses `http://127.0.0.1:8000` as the backend. On other platforms, use the service's private address and container port.

Configure HTTPS, authentication, and any rate limits at the gateway. The API has no built-in authentication; restrict direct access to the backend so callers go through your gateway. CORS only controls browser access and does not authenticate requests.

## 3. Check that it works

Check the running container locally:

```bash
curl --fail http://127.0.0.1:8000/health
```

Expect `{"status":"ok"}`. This lightweight check confirms the API is responding; it does not run an estimation or call external services.

Then try an estimation:

```bash
curl --fail http://127.0.0.1:8000/v1beta/estimations \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": "openai",
    "model_name": "gpt-5.6-luna",
    "output_token_count": 150,
    "request_latency": 1.2,
    "electricity_mix_zone": "USA"
  }'
```

Expect HTTP `200` and a JSON response containing `impacts`. Check that payload for any warnings or errors. Estimation and catalog routes use `/v1beta`, and the model field is `model_name`. Use `/health` for health checks.

Repeat these checks through your company URL, adding the credentials required by your gateway. Configure your applications to call that URL instead of the public EcoLogits API.

## Fully offline deployment in a private VPC

The API uses bundled data and can run without internet access. Follow the deployment steps above, then:

- Build or download a pinned image on a connected machine, then transfer it to your VPC or private registry.
- Use private DNS and an internal gateway with your usual access controls. Authentication, certificates, and logging must also work offline.
- Verify `/health` and an estimation request with internet access blocked.

The `/docs` and `/redoc` pages need public CDN assets. Disable both at deployment by adding `-e DOCS_URL= -e REDOC_URL=` before the image name in your `docker run` command. On other platforms, set `DOCS_URL` and `REDOC_URL` to empty strings. Set only one to disable that page independently.

The API and `/openapi.json` remain available. To keep the documentation pages available offline, [self-host their assets](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).

To update the API or its bundled data, import a new image.

## Keeping it running

Collect container logs and monitor request errors, latency, CPU, and memory. With Docker, view logs using `docker logs ecologits-api`.

The API is stateless, so you can add replicas behind a load balancer without shared storage. Use at least two replicas on separate hosts when you need high availability, and size them using your own load tests.

To upgrade, test the new image in staging, then deploy the same version to production. Keep the previous image and configuration for rollback. EcoLogits updates can change the model catalog and estimation results, so include a few representative estimates in your checks.
