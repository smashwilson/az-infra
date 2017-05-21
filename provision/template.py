import os
from jinja2 import Environment, FileSystemLoader

def mustache(text):
    """
    Jinja2 filter to wrap text in verbatim {{ }}.
    """

    return '{{ ' + text + ' }}'

def template_payload(config):
    """
    Construct a dict that passes selected configuration options to the Jinja template.
    """

    return {
        'pushbot': {
            'branch': config.pushbot_branch,
            'dnd_public_channel': config.pushbot_dnd_public_channel,
            'admins': config.pushbot_admins,
            'betray_immune': config.pushbot_betray_immune
        },
        'secrets': {
            'postgres_url': config.postgres_url,
            'slack_token': config.slack_token,
            'darksky_apikey': config.darksky_apikey,
            'google_cse_id': config.google_cse_id,
            'google_cse_key': config.google_cse_key
        }
    }

def render(config, source):
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
    return template.render(template_payload(config))
