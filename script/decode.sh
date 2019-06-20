#!/bin/bash
#
# Decode authorization failure messages from AWS.

set -euo pipefail

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=script/common.sh
source "${ROOT}/script/common.sh"
load_credentials

docker build -t azurefire-infra:local .
clear
docker run --rm -i \
  -e "AWS_ACCESS_KEY_ID=$DECODE_AWS_ACCESS_KEY_ID" \
  -e "AWS_SECRET_ACCESS_KEY=$DECODE_AWS_SECRET_ACCESS_KEY" \
  azurefire-infra:local \
  decode "$@"
