## Local instalation

```shell
cd tmp/NATTEN && make && pip install .
pip install .
```

## Build

Swap `linux/amd64` and `Dockerfile` with `linux/arm64` and `Dockerfile.mac` for arm-based builds

```shell
docker buildx build --platform linux/amd64 -f Dockerfile -t [url]/music2beats:[tag] .
```

## API Client

```shell
openapi-python-client generate --url http://localhost:30000/openapi.json --overwrite --output-path client
```
