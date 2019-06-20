#!/bin/bash
#
# Launch a shell on pushbot's PostgreSQL database.

set -euo pipefail

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=script/common.sh
source "${ROOT}/script/common.sh"
load_credentials

printf "Connecting to Postgres.\n"
exec docker run --rm -it \
  postgres:9.6 psql "${COORDINATOR_POSTGRES_URL}"
