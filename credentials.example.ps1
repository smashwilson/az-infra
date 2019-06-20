# Copy to credentials.ps1

# AWS account credentials
$env:AWS_ACCESS_KEY_ID = ''
$env:AWS_SECRET_ACCESS_KEY = ''
$env:AWS_DEFAULT_REGION = 'us-east-1'

# Used for script/decode to decode AWS error messages
$env:DECODE_AWS_ACCESS_KEY_ID = ''
$env:DECODE_AWS_SECRET_ACCESS_KEY = ''
$env:DECODE_AWS_REGION = $env:AWS_DEFAULT_REGION

# Used for az-infra notifications
$env:SLACK_WEBHOOK_URL = ''

# az-coordinator options
$env:COORDINATOR_LISTEN_ADDRESS = '0.0.0.0:8443'
$env:COORDINATOR_POSTGRES_URL = 'postgres://me:shhh@localhost/coordinator'
$env:COORDINATOR_AWS_REGION = $env:AWS_DEFAULT_REGION
$env:COORDINATOR_DOCKER_API_VERSION = '1.38'
$env:COORDINATOR_ALLOWED_ORIGIN = 'https://pushbot.party'
$env:COORDINATOR_MASTER_KEY_ID = '' # valid KMS master key ID
$env:COORDINATOR_AUTH_TOKEN = '' # something arbitrary and random
