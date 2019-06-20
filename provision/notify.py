import requests
import os

def begin(context):
    webhook_url = context.config.slack_webhook_url
    requests.post(webhook_url, json={
        'text': 'Infrastructure deployment is <now in progress|https://github.com/smashwilson/az-infra/actions>.'
    })

def success(context):
    webhook_url = context.config.slack_webhook_url

    requests.post(webhook_url, json={
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
    webhook_url = context.config.slack_webhook_url

    requests.post(webhook_url, json={
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
