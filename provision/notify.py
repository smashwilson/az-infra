import urllib.request
import json
import os

def _send_to_slack(context, request_body):
    req = urllib.request.Request(
        method='POST',
        url=context.config.slack_webhook_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(request_body).encode('utf-8')
    )
    urllib.request.urlopen(req)

def begin(context):
    _send_to_slack(context, {
        'text': 'Infrastructure deployment is <now in progress|https://github.com/smashwilson/az-infra/actions>.'
    })

def success(context):
    _send_to_slack(context, {
        'attachments': [
            {
                'fallback': 'azurefire infrastructure deployed successfully.',
                'color': 'good',
                'title': 'Azurefire infrastructure deployed successfully.',
                'title_link': 'https://github.com/smashwilson/az-infra/actions',
                'text': 'Server `{}` launched and bootstrapped in _{}_.'.format(context.instance.id, context.elapsed_time()),
                'mrkdwn_in': ['text']
            }
        ]
    })

def failure(context, formatted_tb):
    _send_to_slack(context, {
        'attachments': [
            {
                'fallback': 'azurefire infrastructure deployment failed.',
                'color': 'danger',
                'title': 'Azurefire infrastructure deployment failed.',
                'title_link': context.build_href(),
                'text': "Here's the stack:\n```\n{}\n```\n".format(formatted_tb),
                'mrkdwn_in': ['text']
            }
        ]
    })
