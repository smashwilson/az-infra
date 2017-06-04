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
  -e POSTGRES_URL `
  -e SLACK_TOKEN `
  -e DARKSKY_APIKEY `
  -e GOOGLE_CSE_ID `
  -e GOOGLE_CSE_KEY `
  -e LE_EMAIL `
  -e SLACK_WEBHOOK_URL `
  -e MAGICAL_WEAK_SPOT_TOKEN `
  -v C:/Users/smash/src/azurefire-infra/out:/usr/src/app/out:rw `
  aaa @argv