## Build

Swap `linux/amd64` with `linux/arm64` for arm-based builds

```shell
docker buildx build --platform linux/arm64 -f Dockerfile.mac -t superduperai/music2beats:arm64 .
```

## API Client

```shell
openapi-python-client generate --url http://localhost:30000/openapi.json --overwrite --output-path client
```
