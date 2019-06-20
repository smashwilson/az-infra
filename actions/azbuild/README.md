# azbuild

This is a GitHub action to build and push specialized Docker containers to [quay.io](https://quay.io). It tags and pushes the built container image with a suffix matching the current git ref, with the exception that `master` becomes `latest`.

| Environment variable | Description |
| --- | --- |
| `DOCKER_REGISTRY_URL` | Docker registry to authenticate and push to |
| `DOCKER_USERNAME` | Docker credentials. |
| `DOCKER_PASSWORD` | Docker credentials. |
