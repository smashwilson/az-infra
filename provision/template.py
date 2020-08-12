import os
import json
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

    coordinator_options = {
        "listen_address": context.config.coordinator_listen_address,
        "database_url": context.config.coordinator_postgres_url,
        "auth_token": context.config.coordinator_auth_token,
        "master_key_id": context.config.coordinator_master_key_id,
        "aws_region": context.config.coordinator_aws_region,
        "docker_api_version": context.config.coordinator_docker_api_version,
        "allowed_origin": context.config.coordinator_allowed_origin,
        "slack_webhook_url": context.config.slack_webhook_url,
    }
    coordinator_options_json = json.dumps(coordinator_options, sort_keys=True, indent=2)

    return {
        'resource': {
            'id': context.config.resource_id
        },
        'az_coordinator': {
            'download_url': context.az_coordinator_download_url,
            'options_json': coordinator_options_json
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
