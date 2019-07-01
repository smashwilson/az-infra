# azsync

This is a GitHub action to build and push specialized Docker containers to [quay.io](https://quay.io). It tags and pushes the built container image with a suffix matching the current git ref, with the exception that `master` becomes `latest`.

| Environment variable | Description |
| --- | --- |
| `AZ_COORDINATOR_TOKEN` | Authentication token for the [az-coordinator](https://github.com/smashwilson/az-coordinator) |
