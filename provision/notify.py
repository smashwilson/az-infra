import requests

def begin(context):
    webhook_url = context.config.slack_webhook_url
    message = context.config.message
    if not message:
        message = os.environ.get('TRAVIS_COMMIT_MESSAGE', '(unknown)')
    requests.post(webhook_url, json={
        'text': 'Infrastructure deployment is <{}|now in progress>.\n_{}_'.format(
            context.build_href(),
            message
        )
    })

def success(context):
    webhook_url = context.config.slack_webhook_url
    bootstrap_result = context.bootstrap_result

    fields = []
    for (name, service) in bootstrap_result.services():
        github_url = 'https://github.com/smashwilson/{}/commit/{}'.format(name, service['git_commit'])
        github_short = '{} @ {}'.format(context.service_git_branch(name), service['git_commit'][0:8])

        quay_url = 'https://quay.io/repository/smashwilson/{}/image/{}'.format(name, service['image_id'])
        quay_short = '{} @ {}'.format(context.service_image_tag(name), service['image_id'][0:8])

        fields.append({
            'title': name,
            'value': ':octocat: <{}|{}> :docker: <{}|{}>'.format(github_url, github_short, quay_url, quay_short)
        })

    requests.post(webhook_url, json={
        'attachments': [
            {
                'fallback': 'azurefire infrastructure deployed successfully.',
                'color': 'good',
                'title': 'Azurefire infrastructure deployed successfully.',
                'title_link': context.build_href(),
                'text': 'Server `{}` launched and bootstrapped in _{}_.'.format(context.instance.id, context.elapsed_time()),
                'mrkdwn_in': ['text'],
                'fields': fields
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
