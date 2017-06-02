import os
from jinja2 import Environment, FileSystemLoader

def mustache(text):
    """
    Jinja2 filter to wrap text in verbatim {{ }}.
    """

    return '{{ ' + text + ' }}'

def template_payload(context):
    """
    Construct a dict that passes selected configuration options to the Jinja template.
    """

    if context.elb_targets:
        prior_addresses = ','.join(i['IpAddr'] for i in context.elb_targets)
    else:
        prior_addresses = ''

    return {
        'pushbot': {
            'branch': context.config.pushbot_branch,
            'dnd_public_channel': context.config.pushbot_dnd_public_channel,
            'admins': context.config.pushbot_admins,
            'betray_immune': context.config.pushbot_betray_immune,
            'prior_addresses': prior_addresses
        },
        'nginx': {
            'branch': context.config.azurefire_nginx_branch
        },
        'tls': {
            'branch': context.config.azurefire_tls_branch
        },
        'letsencrypt': {
            'email': context.config.le_email
        },
        'secrets': {
            'postgres_url': context.config.postgres_url,
            'slack_token': context.config.slack_token,
            'darksky_apikey': context.config.darksky_apikey,
            'google_cse_id': context.config.google_cse_id,
            'google_cse_key': context.config.google_cse_key,
            'magical_weak_spot_token': context.config.magical_weak_spot_token
        }
    }

def render(context, source):
    """
    Initialize a Jinja2 environment and use it to render a template in the template/ directory.
    """

    loader = FileSystemLoader(
        os.path.join(os.path.dirname(__file__), '..', 'template')
    )
    env = Environment(
        loader=loader,
        autoescape=False,
        auto_reload=False
    )
    env.filters['mustache'] = mustache

    template = env.get_template(source)
    return template.render(template_payload(context))
