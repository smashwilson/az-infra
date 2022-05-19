# azsync

This is a GitHub action to trigger the [Azurefire coordinator](https://github.com/smashwilson/az-coordinator) to perform a synchronization action, which will pull the latest container images and restart any running containers that have changed.

| Environment variable | Description |
| --- | --- |
| `AZ_COORDINATOR_TOKEN` | Authentication token for the [az-coordinator](https://github.com/smashwilson/az-coordinator) |
