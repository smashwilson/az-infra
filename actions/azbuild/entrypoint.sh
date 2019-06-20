#!/bin/sh

set -eu

if [ -z "${GITHUB_REF:-}" ]; then
  printf "No ref available.\n"
  exit 78
fi

SHORT_REF=$(basename ${GITHUB_REF})
IMAGE_NAME=${DOCKER_REGISTRY_URL}/${GITHUB_REPOSITORY}

if [ "${GITHUB_REF:-}" = "refs/heads/master" ]; then IMAGE_TAG=latest; else IMAGE_TAG="${SHORT_REF}"; fi

printf "Authenticating to Docker registry.\n"
docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD} ${DOCKER_REGISTRY_URL}

printf "Bulding Docker container (%s:%s).\n" "${IMAGE_NAME}" "${IMAGE_TAG}"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .

printf "Pushing Docker container.\n"
docker push "${IMAGE_NAME}:${IMAGE_TAG}"
