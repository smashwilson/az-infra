import re
from datetime import datetime, timedelta

from provision.config import Config

class Context:
    def __init__(self, args):
        self.start_ts = datetime.utcnow()
        self.config = Config(args)

        self.elb_security_group = None
        self.elb_targets = None

        self.key_pair = None
        self.security_group = None
        self.instance = None

        self.bootstrap_result = None

    def make_name(self, base):
        return 'azurefire_' + base + '_' + str(self.config.resource_id)

    def make_tags(self):
        return [
            {'Key': 'Purpose', 'Value': 'pushbot'},
            {'Key': 'Build', 'Value': str(self.config.build_id)},
            {'Key': 'Resource', 'Value': str(self.config.resource_id)},
            {'Key': 'Name', 'Value': self.build_name()}
        ]

    def accept_bootstrap_stdout(self, bootstrap_stdout):
        self.bootstrap_result = BootstrapResult()
        self.bootstrap_result.parse_from(bootstrap_stdout)

    def build_name(self):
        return 'azurefire-{}'.format(self.config.resource_id)

    def service_git_branch(self, service_name):
        tag = self.service_image_tag(service_name)
        if tag == 'latest':
            return 'master'
        else:
            return tag

    def service_image_tag(self, service_name):
        normalized_name = service_name.replace('-', '_')
        return getattr(self.config, '{}_tag'.format(normalized_name))

    def build_href(self):
        return 'https://travis-ci.org/smashwilson/azurefire-infra/builds/{}'.format(self.config.build_id)

    def elapsed_time(self):
        delta = datetime.utcnow() - self.start_ts
        parts = []

        def handle_unit(remaining, unit_delta, name):
            if remaining > unit_delta:
                quantity = delta // unit_delta
                part = str(quantity)
                part += ' ' + name
                if quantity != 0:
                    part += 's'
                parts.append(part)
                return remaining - (quantity * unit_delta)
            else:
                return remaining

        delta = handle_unit(delta, timedelta(hours=1), 'hour')
        delta = handle_unit(delta, timedelta(minutes=1), 'minute')
        handle_unit(delta, timedelta(seconds=1), 'second')

        return ' '.join(parts)

class BootstrapResult:
    def __init__(self):
        self.service_specs = {}

    def parse_from(self, bootstrap_stdout):
        matches = re.findall('\n>> (\S+) (?:sha256:)?(\S+) (\S+)', bootstrap_stdout)
        for (service, image_id, git_commit) in matches:
            self.service_specs[service] = {
                'image_id': image_id,
                'git_commit': git_commit.strip()
            }

    def services(self):
        return self.service_specs.items()
