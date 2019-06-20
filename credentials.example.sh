#!/bin/sh
#
# Copy to credentials.sh

# AWS account credentials
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=us-east-1

# Used for script/decode to decode AWS error messages
export DECODE_AWS_ACCESS_KEY_ID=
export DECODE_AWS_SECRET_ACCESS_KEY=

# Let's Encrypt account information
export LE_EMAIL=whatever@somewhere.com

# Database connection
export PUSHBOT_POSTGRES_URL=postgres://me:shhh@localhost/pushbot
export COORDINATOR_POSTGRES_URL=postgres://me:shhh@localhost/coordinator

# Account tokens and API keys
export SLACK_TOKEN=
export TRAVIS_TOKEN=
export SLACK_WEBHOOK_URL=
export DARKSKY_APIKEY=
export GOOGLE_CSE_ID=
export GOOGLE_CSE_KEY=

# Set this to something nice and random so random people can't take down your
# bot with a well-placed DELETE request
export MAGICAL_WEAK_SPOT_TOKEN=
