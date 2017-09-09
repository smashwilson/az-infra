#!/bin/bash
#
# CI script for use by service container repositories. Download and execute
# this script from another Travis environment to:
#
# * Build and push a Docker container to quay.io/smashwilson/... for each
#   branch and (privileged) pull request.
#
# * If the current branch is active in azurefire-infra, trigger a rebuild
#   of the latest azurefire-infra master to deploy the newly pushed
#   container to azurefire.

set -euo pipefail

# Collect and summarize information from the environment into variables for use
# by other build phases.
info() {
  if [ -z "${SERVICE_NAME:-}" ]; then
    if [ -z "${TRAVIS_REPO_SLUG}" ]; then
      printf "Unable to infer SERVICE_NAME.\n" >&2
      return 1
    fi

    SERVICE_NAME="${TRAVIS_REPO_SLUG#*/}"
  fi

  IMAGE_BASE="quay.io/smashwilson/${SERVICE_NAME}"

  TAG=
  if [ "${TRAVIS_PULL_REQUEST:-}" = "false" ]; then
    if [ "${TRAVIS_BRANCH:-}" = "master" ]; then
      TAG="latest"
    else
      TAG="${TRAVIS_BRANCH:-local}"
    fi
  elif [ -n "${TRAVIS_PULL_REQUEST:-}" ]; then
    TAG="pr${TRAVIS_PULL_REQUEST}"
  else
    TAG="local"
  fi

  IMAGE_TAG="${IMAGE_BASE}:${TAG}"
}

# Invoke during the script: phase. Build the docker image, failing the build if
# the docker build fails.
build() {
  info

  printf "Building container image ${IMAGE_TAG}.\n"

  docker build \
    --tag "${IMAGE_TAG}" \
    --label party.pushbot.commit=$(git rev-parse HEAD) \
    .
}

# Invoke during the after_success: phase. Push the built docker image to
# quay.io if credentials are present.
after_success() {
  if [ -z "${DOCKER_USERNAME:-}" ] || [ -z "${DOCKER_PASSWORD:-}" ]; then
    printf "Docker credentials not present.\n"
    printf "Skipping image push for this build.\n"
    return 0
  fi

  info

  printf "Authenticating to Quay.\n"
  docker login -u "${DOCKER_USERNAME}" -p "${DOCKER_PASSWORD}" quay.io

  printf "Pushing container image ${IMAGE_TAG} to Quay.\n"
  docker push "${IMAGE_TAG}"
}

# Invoke from a deploy: phase. Trigger a rebuild of the latest pull request
# build on the azurefire-infra repository.
deploy() {
  if [ -z "${TRAVIS_TOKEN:-}" ]; then
    printf "TRAVIS_TOKEN is not specified for this build.\n" >&2
    exit 1
  fi

  info

  printf "Checking the active azurefire-infra configuration.\n"
  curl https://raw.githubusercontent.com/smashwilson/azurefire-infra/master/config.json \
    -o config.json

  DEPLOYED_TAG=$(jq --raw-output ".[\"${SERVICE_NAME}\"].tag" < config.json)
  if [ "${DEPLOYED_TAG}" != "${TAG}" ]; then
    printf "Tag %s is currently deployed, not %s.\n" "${DEPLOYED_TAG}" "${TAG}"
    return 0
  fi

  BODY='{
    "request": {
      "branch": "master",
      "config": {
        "merge_mode": "deep_merge",
        "env": [
          "BUILD_CAUSE=:arrow_up: '${TRAVIS_REPO_SLUG}'"
        ]
      }
    }
  }'
  printf "Triggering an infrastructure rebuild.\n"
  curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "Travis-API-Version: 3" \
    -H "Authorization: token ${TRAVIS_TOKEN}" \
    -d "${BODY}" \
    https://api.travis-ci.org/repo/smashwilson%2Fazurefire-infra/requests
}

case "${1:-}" in
  build) build ;;
  after_success) after_success ;;
  deploy) deploy ;;
  *)
    printf "Unrecognized command: %s\n" "${1:-}" >&2
    printf "Please specify one of build, after_success, or deploy.\n" >&2
    exit 1
    ;;
esac
