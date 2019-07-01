#!/bin/sh

set -eu

exec curl --silent -i -X POST https://u:${AZ_COORDINATOR_TOKEN}@coordinator.azurefire.net:8443/sync
