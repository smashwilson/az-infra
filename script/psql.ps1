# Launch a shell on pushbot's PostgreSQL database.

. .\credentials.ps1

Write-Output "Connecting to Postgres."
docker run --rm -it `
  postgres:9.6 psql $env:POSTGRES_URL
