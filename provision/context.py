import re

from provision.config import Config

class Context:
    def __init__(self, args):
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

class BootstrapResult:
    def __init__(self):
        self.service_specs = {}

    def parse_from(self, bootstrap_stdout):
        matches = re.findall('\n>> (\S+) (\S+) (\S+)', bootstrap_stdout)
        for (service, image_id, git_commit) in matches:
            self.service_specs[service] = {
                'image_id': image_id,
                'git_commit': git_commit.strip()
            }

    def services(self):
        return this.service_specs.iter_items()
