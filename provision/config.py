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

        # Loaded from config.json
        self.server_image_id = public_config['server']['image_id']
        self.server_instance_type = public_config['server']['instance_type']
        self.server_ssh_timeout = public_config['server']['ssh_timeout']
        self.server_instance_profile_arn = public_config['server']['instance_profile_arn']
        self.server_instance_az = public_config['server']['instance_az']
        self.rds_security_group_id = public_config['rds']['security_group_id']
        self.bootstrap_timeout = public_config['bootstrap']['timeout']

        # Loaded from credentials.sh
        self.elastic_ip_id = os.environ['ELASTIC_IP_ID']
        self.slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
        self.coordinator_listen_address = os.environ['COORDINATOR_LISTEN_ADDRESS']
        self.coordinator_postgres_url = os.environ['COORDINATOR_POSTGRES_URL']
        self.coordinator_aws_region = os.environ['COORDINATOR_AWS_REGION']
        self.coordinator_docker_api_version = os.environ['COORDINATOR_DOCKER_API_VERSION']
        self.coordinator_allowed_origin = os.environ['COORDINATOR_ALLOWED_ORIGIN']
        self.coordinator_master_key_id = os.environ['COORDINATOR_MASTER_KEY_ID']
        self.coordinator_auth_token = os.environ['COORDINATOR_AUTH_TOKEN']

        self.resource_id = int(time.time())

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
