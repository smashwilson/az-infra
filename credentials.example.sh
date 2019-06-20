#!/bin/sh
#
# Copy to credentials.sh

# AWS account credentials used for provisioning
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=us-east-1

# Used for script/decode to decode AWS error messages
export DECODE_AWS_ACCESS_KEY_ID=
export DECODE_AWS_SECRET_ACCESS_KEY=
export DECODE_AWS_REGION="${AWS_DEFAULT_REGION}"

# Allocation ID of an Elastic IP address bound to azurefire hosts
export ELASTIC_IP_ID=

# Used for az-infra notifications
export SLACK_WEBHOOK_URL=

# az-coordinator options
export COORDINATOR_LISTEN_ADDRESS=0.0.0.0:8443
export COORDINATOR_POSTGRES_URL=postgres://me:shhh@localhost/coordinator
export COORDINATOR_AWS_REGION="${AWS_DEFAULT_REGION}"
export COORDINATOR_DOCKER_API_VERSION=1.38
export COORDINATOR_ALLOWED_ORIGIN=https://pushbot.party
export COORDINATOR_MASTER_KEY_ID= # valid KMS master key ID
export COORDINATOR_AUTH_TOKEN= # something arbitrary and random
