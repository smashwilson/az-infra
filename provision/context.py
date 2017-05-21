from provision.config import Config

class Context:
    def __init__(self):
        self.config = Config()

        self.key_pair = None
        self.security_group = None
        self.instance = None

    def make_name(self, base):
        return base + '_' + self.config.build_no
