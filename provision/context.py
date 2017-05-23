from provision.config import Config

class Context:
    def __init__(self, args):
        self.config = Config(args)

        self.key_pair = None
        self.security_group = None
        self.instance = None

    def make_name(self, base):
        return base + '_' + self.config.build_no

    def make_tags(self):
        return [
            {'Key': 'purpose', 'Value': 'pushbot'},
            {'Key': 'build', 'Value': str(self.config.build_no)}
        ]
