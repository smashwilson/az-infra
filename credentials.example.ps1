# Copy to credentials.ps1

# AWS account credentials
$env:AWS_ACCESS_KEY_ID = ''
$env:AWS_SECRET_ACCESS_KEY = ''
$env:AWS_DEFAULT_REGION = 'us-east-1'

$env:DECODE_AWS_ACCESS_KEY_ID = ''
$env:DECODE_AWS_SECRET_ACCESS_KEY = ''

# Let's Encrypt account information
$env:LE_EMAIL = 'whatever@somewhere.com'

# Database connection
$env:POSTGRES_URL = 'postgres://me:shhh@localhost/dbname'

# Account tokens and API keys
$env:SLACK_TOKEN = ''
$env:SLACK_WEBHOOK_URL = ''
$env:DARKSKY_APIKEY = ''
$env:GOOGLE_CSE_ID = ''
$env:GOOGLE_CSE_KEY = ''

# Set this to something nice and random so random people can't take down your
# bot with a well-placed DELETE request
$env:MAGICAL_WEAK_SPOT_TOKEN = ''
