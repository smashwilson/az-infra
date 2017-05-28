import re
from datetime import datetime, timedelta

from provision.config import Config

class Context:
    def __init__(self, args):
        self.start_ts = datetime.utcnow()
        self.config = Config(args)

        self.key_pair = None
        self.security_group = None
        self.instance = None

        self.bootstrap_result = None

    def make_name(self, base):
        return 'azurefire_' + base + '_' + self.config.build_no

    def make_tags(self):
        return [
            {'Key': 'purpose', 'Value': 'pushbot'},
            {'Key': 'build', 'Value': str(self.config.build_no)},
            {'Key': 'Name', 'Value': 'azurefire-{}'.format(self.config.build_no)}
        ]

    def accept_bootstrap_stdout(self, bootstrap_stdout):
        self.bootstrap_result = BootstrapResult()
        self.bootstrap_result.parse_from(bootstrap_stdout)

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
