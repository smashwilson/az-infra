#!/bin/bash
#
# Sourced from other scripts to make useful scripts available.

set -euo pipefail

if [ -z "${ROOT:-}" ]; then
  printf "[ERROR] ROOT is not defined before common.sh was sourced.\n" >&2
  exit 1
fi

load_credentials() {
  local -a CREDFILE_LOCATIONS=("${ROOT}/credentials.sh" "/keybase/private/${USER}/az-infra/credentials.sh")

  for LOCATION in "${CREDFILE_LOCATIONS[@]}"; do
    if [ -f "${LOCATION}" ]; then
      # shellcheck source=/dev/null
      source "${LOCATION}"
      return
    fi
  done

  printf "[ERROR] %s/credentials.sh not found.\n" "${ROOT}/credentials.sh" >&2
  printf "[ERROR] Please run 'cp credentials.example.sh credentials.sh' and try again.\n" >&2
  exit 1
}
