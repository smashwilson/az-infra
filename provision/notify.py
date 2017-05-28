import requests

def success(context):
    webhook_url = context.config.slack_webhook_url
    bootstrap_result = context.bootstrap_result

    fields = []
    for (name, service) in bootstrap_result.services():
        github_url = 'https://github.com/smashwilson/{}/commit/{}'.format(name, service['git_commit'])
        github_short = context.service_git_branch(name)

        quay_url = 'https://quay.io/repository/smashwilson/{}/image/{}'.format(name, service['image_id'])
        quay_short = context.service_image_tag(name)

        fields.append({
            'title': name,
            'value': ':octocat: <{}|{}> :docker: <{}|{}>'.format(github_url, github_short, quay_url, quay_short)
        })

    requests.post(webhook_url, json={
        'username': 'azurefire',
        'icon_emoji': ':shipit:',
        'attachments': [
            {
                'fallback': 'azurefire infrastructure deployed successfully.',
                'color': 'good',
                'title': 'Azurefire infrastructure deployed successfully.',
                'title_link': '',
                'text': 'Server `{}` launched and bootstrapped in _{}_.'.format(context.instance.id, context.elapsed_time()),
                'mrkdwn_in': ['text'],
                'fields': fields
            }
        ]
    })

def failure(context, formatted_tb):
    requests.post(webhook_url, json={
        'username': 'azurefire',
        'icon_emoji': ':rotating_light:',
        'attachments': [
            {
                'fallback': 'azurefire infrastructure deployment failed.',
                'color': 'bad',
                'title': 'Azurefire infrastructure deployment failed.',
                'title_link': '',
                'text': "Here's the stack:\n```\n{}\n```\n".format(formatted_tb),
                'mrkdwn_in': ['text']
            }
        ]
    })
