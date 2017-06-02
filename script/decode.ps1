# Decode authorization failure messages from AWS.

[CmdletBinding()]
Param(
  [Parameter(Mandatory=$True)]
  [string]$message
)

. .\credentials.ps1

docker build -t aaa .
docker run --rm -i `
  -e "AWS_ACCESS_KEY_ID=$env:DECODE_AWS_ACCESS_KEY_ID" `
  -e "AWS_SECRET_ACCESS_KEY=$env:DECODE_AWS_SECRET_ACCESS_KEY" `
  aaa decode $message
