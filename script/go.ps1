# Provision a new deployment using the credentials in credentials.ps1.

[CmdletBinding()]
Param(
  [parameter(mandatory=$false, position=1, ValueFromRemainingArguments=$true)]
  $argv
)

. .\credentials.ps1

docker build -t aaa .
cls
docker run --rm `
  -e AWS_ACCESS_KEY_ID `
  -e AWS_SECRET_ACCESS_KEY `
  -e AWS_DEFAULT_REGION `
  -e ELASTIC_IP_ID `
  -e SLACK_WEBHOOK_URL `
  -e MAGICAL_WEAK_SPOT_TOKEN `
  -e COORDINATOR_LISTEN_ADDRESS `
  -e COORDINATOR_POSTGRES_URL `
  -e COORDINATOR_AWS_REGION `
  -e COORDINATOR_DOCKER_API_VERSION `
  -e COORDINATOR_ALLOWED_ORIGIN `
  -e COORDINATOR_MASTER_KEY_ID `
  -e COORDINATOR_AUTH_TOKEN `
  -v C:/Users/smash/src/azurefire-infra/out:/usr/src/app/out:rw `
  aaa @argv
