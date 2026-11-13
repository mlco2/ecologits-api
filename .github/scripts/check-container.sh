#!/usr/bin/env bash
set -euo pipefail

image="${1:-ecologits-api:ci}"
container_id=$(docker run -d --cap-drop=ALL -p 127.0.0.1::8000 "$image")
cleanup() {
  status=$?
  if [ "$status" -ne 0 ]; then
    docker logs "$container_id" || true
  fi
  docker rm -f "$container_id" >/dev/null
}
trap cleanup EXIT

address=$(docker port "$container_id" 8000/tcp)
curl --fail --silent --show-error --retry 30 --retry-all-errors \
  --retry-delay 1 --retry-max-time 45 --max-time 5 \
  --output /dev/null "http://$address/v1beta/providers"

docker exec -i "$container_id" /app/.venv/bin/python - <<'PY'
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import sys
import urllib.request

assert os.getuid() == os.getgid() == 10001
assert set(Path('/proc/1/status').read_text().split('Uid:')[1].splitlines()[0].split()) == {'10001'}
assert os.environ['PYTHONUNBUFFERED'] == '1'
assert sys.stdout.write_through
for tool in ('uv', 'uvx', 'ruff', 'pytest'):
    assert shutil.which(tool) is None, tool
for package in ('ruff', 'pytest'):
    try:
        importlib.metadata.distribution(package)
    except importlib.metadata.PackageNotFoundError:
        pass
    else:
        raise AssertionError(f'{package} is installed')
assert set(os.listdir('/app')) == {'app', '.venv', 'pyproject.toml', 'uv.lock'}
assert not list(Path('/app').rglob('.env*'))
assert not list(Path('/app').rglob('.work'))
print('Runtime checks passed; EcoLogits', importlib.metadata.version('ecologits'))

base = 'http://127.0.0.1:8000'
for path in ('/docs', '/openapi.json', '/v1beta/providers', '/v1beta/models/openai', '/v1beta/electricity-mix-zones/WOR'):
    with urllib.request.urlopen(base + path, timeout=10) as response:
        assert response.status == 200
    print(f'GET {path}: 200')
payload = json.dumps(dict(provider='openai', model_name='gpt-4o-mini', output_token_count=150, request_latency=1.2, electricity_mix_zone='WOR')).encode()
request = urllib.request.Request(base + '/v1beta/estimations', data=payload, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(request, timeout=10) as response:
    assert response.status == 200
    assert json.load(response)['impacts'] is not None
print('POST /v1beta/estimations: 200')
PY
