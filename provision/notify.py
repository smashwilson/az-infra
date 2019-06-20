import urllib.request
import json
import os

def begin(context):
    req = urllib.request.Request(
        method='POST',
        url=context.config.slack_webhook_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'text': 'Infrastructure deployment is <now in progress|https://github.com/smashwilson/az-infra/actions>.'
        })
    )
    urllib.request.urlopen(req)

def success(context):
    req = urllib.request.Request(
        method='POST',
        url=context.config.slack_webhook_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
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
    )
    urllib.request.urlopen(req)

def failure(context, formatted_tb):
    req = urllib.request.Request(
        method='POST',
        url=context.config.slack_webhook_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
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
    )
    urllib.request.urlopen(req)
