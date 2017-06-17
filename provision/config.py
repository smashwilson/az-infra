import os
import json
import argparse
import time

from enum import Enum

class Action(Enum):
    PROVISION = 1
    DELETE = 2

class Config:

    def __init__(self, args):
        with open('config.json', 'r') as cf:
            public_config = json.load(cf)

        self.loadbalancer_name = public_config['loadbalancer']['name']

        self.image_id = public_config['server']['image_id']
        self.instance_type = public_config['server']['instance_type']
        self.ssh_attempts = public_config['server']['ssh_timeout']
        self.instance_profile_arn = public_config['server']['instance_profile_arn']
        self.instance_az = public_config['server']['instance_az']

        self.rds_security_group_id = public_config['rds']['security_group_id']
        self.bootstrap_timeout = public_config['bootstrap']['timeout']
        self.pushbot_tag = public_config['pushbot']['tag']
        self.pushbot_admins = public_config['pushbot']['admins']
        self.pushbot_betray_immune = public_config['pushbot']['betray_immune']
        self.pushbot_dnd_public_channel = public_config['pushbot']['betray_immune']
        self.pushbot_slack_team_id = public_config['pushbot']['slack_team_id']
        self.pushbot_api_base_url = public_config['pushbot']['api_base_url']
        self.pushbot_web_base_url = public_config['pushbot']['web_base_url']

        self.azurefire_nginx_tag = public_config['azurefire-nginx']['tag']
        self.azurefire_tls_tag = public_config['azurefire-tls']['tag']

        self.resource_id = int(time.time())
        self.build_id = os.environ.get('TRAVIS_BUILD_ID', '0')

        self.le_email = os.environ['LE_EMAIL']
        self.postgres_url = os.environ['POSTGRES_URL']
        self.slack_token = os.environ['SLACK_TOKEN']
        self.slack_client_id = os.environ['SLACK_CLIENT_ID']
        self.slack_client_secret = os.environ['SLACK_CLIENT_SECRET']
        self.darksky_apikey = os.environ['DARKSKY_APIKEY']
        self.google_cse_id = os.environ['GOOGLE_CSE_ID']
        self.google_cse_key = os.environ['GOOGLE_CSE_KEY']
        self.session_secret = os.environ['SESSION_SECRET']
        self.magical_weak_spot_token = os.environ['MAGICAL_WEAK_SPOT_TOKEN']

        self.slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--resource-id', help='Override the resource ID')
        parser.add_argument('-d', '--delete', action='store_true', help='Delete all pushbot resources on the account')
        options = parser.parse_args(args[1:])

        if options.resource_id:
            self.resource_id = options.resource_id

        if options.delete:
            self.action = Action.DELETE
        else:
            self.action = Action.PROVISION
