import os
import configparser
import argparse

from enum import Enum

class Action(Enum):
    PROVISION = 1
    DELETE = 2

class Config:

    def __init__(self, args):
        public_ini = configparser.ConfigParser()
        public_ini.read('config.ini')

        self.image_id = public_ini.get('server', 'image_id')
        self.instance_type = public_ini.get('server', 'instance_type')
        self.ssh_attempts = public_ini.getint('server', 'ssh_timeout') / 10
        self.instance_profile_arn = public_ini.get('server', 'instance_profile_arn')
        self.rds_security_group_id = public_ini.get('rds', 'security_group_id')
        self.bootstrap_timeout = public_ini.getint('bootstrap', 'timeout')
        self.pushbot_branch = public_ini.get('pushbot', 'branch')
        self.pushbot_admins = public_ini.get('pushbot', 'admins')
        self.pushbot_betray_immune = public_ini.get('pushbot', 'betray_immune')
        self.pushbot_dnd_public_channel = public_ini.get('pushbot', 'betray_immune')

        self.azurefire_nginx_branch = public_ini.get('nginx', 'branch')
        self.azurefire_tls_branch = public_ini.get('tls', 'branch')

        self.build_no = os.environ.get('TRAVIS_JOB_NUMBER', '0')
        self.le_email = os.environ['LE_EMAIL']
        self.postgres_url = os.environ['POSTGRES_URL']
        self.slack_token = os.environ['SLACK_TOKEN']
        self.darksky_apikey = os.environ['DARKSPY_APIKEY']
        self.google_cse_id = os.environ['GOOGLE_CSE_ID']
        self.google_cse_key = os.environ['GOOGLE_CSE_KEY']

        self.slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

        parser = argparse.ArgumentParser()
        parser.add_argument('-b', '--build-no', help='Override the build number')
        parser.add_argument('-d', '--delete', action='store_true', help='Delete all pushbot resources on the account')
        options = parser.parse_args(args[1:])

        if options.build_no:
            self.build_no = options.build_no

        if options.delete:
            self.action = Action.DELETE
        else:
            self.action = Action.PROVISION
