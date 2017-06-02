#!/bin/bash
# Decode authorization failure messages from AWS.

source ./credentials.sh

docker build -t aaa .
docker run --rm -i \
  -e "AWS_ACCESS_KEY_ID=$DECODE_AWS_ACCESS_KEY_ID" \
  -e "AWS_SECRET_ACCESS_KEY=$DECODE_AWS_SECRET_ACCESS_KEY" \
  aaa decode "$@"
