#!/bin/sh

set -eu

if [ -z "${GITHUB_REF:-}" ]; then
  printf "No ref available.\n"
  exit 78
fi

SHORT_REF=$(basename ${GITHUB_REF})
if [ -z "${IMAGE_NAME:-}" ]; then
  if [ -z "${DOCKER_REGISTRY_URL:-}" ]; then
    IMAGE_NAME="${GITHUB_REPOSITORY}"
  else
    IMAGE_NAME=${DOCKER_REGISTRY_URL}/${GITHUB_REPOSITORY}
  fi
fi

if [ "${GITHUB_REF:-}" = "refs/heads/main" ] || [ "${GITHUB_REF:-}" = "refs/heads/master" ]; then
  IMAGE_TAG=latest
else
  IMAGE_TAG="${SHORT_REF}"
fi

printf "Authenticating to Docker registry.\n"
printf "${DOCKER_PASSWORD}" | docker login -u ${DOCKER_USERNAME} --password-stdin "${DOCKER_REGISTRY_URL:-}"

printf "Bulding Docker container (%s:%s).\n" "${IMAGE_NAME}" "${IMAGE_TAG}"
docker build \
  --label net.azurefire.repository=${GITHUB_REPOSITORY} \
  --label net.azurefire.commit=${GITHUB_SHA} \
  --label net.azurefire.ref=${GITHUB_REF##refs/heads/} \
  -t "${IMAGE_NAME}:${IMAGE_TAG}" \
  .

printf "Pushing Docker container.\n"
docker push "${IMAGE_NAME}:${IMAGE_TAG}"
