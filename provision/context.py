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

        self.az_coordinator_download_url = None

    def make_name(self, base):
        return 'azurefire_' + base + '_' + str(self.config.resource_id)

    def make_tags(self):
        return [
            {'Key': 'Purpose', 'Value': 'azinfra'},
            {'Key': 'Build', 'Value': str(self.config.build_id)},
            {'Key': 'Resource', 'Value': str(self.config.resource_id)},
            {'Key': 'Name', 'Value': self.build_name()}
        ]

    def build_name(self):
        return 'azurefire-{}'.format(self.config.resource_id)

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
