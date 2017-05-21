import os
import configparser

class Config:

    def __init__(self):
        public_ini = configparser.ConfigParser()
        public_ini.read('config.ini')

        self.image_id = public_ini.get('server', 'image_id')
        self.instance_type = public_ini.get('server', 'instance_type')
        self.ssh_attempts = public_ini.getint('server', 'ssh_timeout') / 10
        self.rds_security_group_id = public_ini.get('rds', 'security_group_id')
        self.bootstrap_timeout = public_ini.getint('bootstrap', 'timeout')
        self.pushbot_branch = public_ini.get('pushbot', 'branch')
        self.pushbot_admins = public_ini.get('pushbot', 'admins')
        self.pushbot_betray_immune = public_ini.get('pushbot', 'betray_immune')
        self.pushbot_dnd_public_channel = public_ini.get('pushbot', 'betray_immune')

        self.build_no = os.environ.get('TRAVIS_JOB_NUMBER', '0')
        self.postgres_url = os.environ['POSTGRES_URL']
        self.slack_token = os.environ['SLACK_TOKEN']
        self.darksky_apikey = os.environ['DARKSPY_APIKEY']
        self.google_cse_id = os.environ['GOOGLE_CSE_ID']
        self.google_cse_key = os.environ['GOOGLE_CSE_KEY']
