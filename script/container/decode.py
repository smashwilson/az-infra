#!/usr/bin/env python

import sys
import boto3
import json

message = sys.argv[1]
client = boto3.client('sts')
response = client.decode_authorization_message(
    EncodedMessage=message
)
document = json.loads(response['DecodedMessage'])
print(json.dumps(document, indent=2))
