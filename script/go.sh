#!/bin/bash
# Provision a new deployment using the credentials in credentials.ps1.

set -euo pipefail

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"

# shellcheck source=script/common.sh
source "${ROOT}/script/common.sh"
load_credentials

docker build -t azurefire-infra:local .
clear
docker run --rm \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  -e AWS_DEFAULT_REGION \
  -e ELASTIC_IP_ID \
  -e SLACK_WEBHOOK_URL \
  -e COORDINATOR_LISTEN_ADDRESS \
  -e COORDINATOR_POSTGRES_URL \
  -e COORDINATOR_AWS_REGION \
  -e COORDINATOR_DOCKER_API_VERSION \
  -e COORDINATOR_ALLOWED_ORIGIN \
  -e COORDINATOR_MASTER_KEY_ID \
  -e COORDINATOR_AUTH_TOKEN \
  -v "$(pwd)/out:/usr/src/app/out:rw" \
  azurefire-infra:local "$@"
