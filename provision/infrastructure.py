import os
import configparser
import subprocess
from output import info, success

import boto3
from jinja2 import Environment, FileSystemLoader

class Context:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.build_no = os.environ.get('TRAVIS_JOB_NUMBER', '0')

        self.ec2 = boto3.resource('ec2')

        loader = FileSystemLoader(
            os.path.join(os.path.dirname(__file__), '..', 'template')
        )
        self.env = Environment(
            loader=loader,
            autoescape=False,
            auto_reload=False,
        )

        self.key_name = self.make_name('key')
        self.instance = None

    def make_name(base):
        return base + '_' + self.build_no

    def template_payload():
        return {
            'pushbot': {
                'branch': 'k8s_and_postgres',
                'dnd_public_channel': '',
                'admins': '',
                'betray_immune': ''
            },
            'secrets': {
                'postgres_url': '',
                'slack_token': '',
                'darksky_apikey': '',
                'google_cse_id': '',
                'google_cse_key': ''
            }
        }

def ssh_key(context):
    """
    Generate a temporary SSH key and upload it to AWS.
    """

    info('Generating SSH key')
    command = [
        'ssh-keygen',
        '-t', 'rsa',
        '-b', '4096',
        '-C', 'burner-key@azurefire.net',
        '-N', '',
        '-f', os.path.join('secrets', 'id_rsa'),
    ]
    subprocess.run(command, check=True)
    with open(os.path.join('secrets', 'id_rsa.pub'), 'rb') as keyfile:
        pub_key_material = keyfile.read()
    success('SSH key generated')

    info('Uploading SSH key to AWS')
    context.ec2.import_key_pair(
        KeyName=context.key_name,
        PublicKeyMaterial=pub_key_material
    )
    success('SSH key uploaded')

def server(context):
    """
    Launch a CoreOS server.
    """

    info('Creating server')
    instance = context.ec2.create_instances(
        ImageId=context.config.get('server', 'image_id'),
        MinCount=1,
        MaxCount=1,
        KeyName=context.key_name,
        InstanceType=context.config.get('server', 'instance_type'),
        TagSpecifications=[
            {'ResourceType': 'instance', 'Tags': [{'Key': 'creation', 'Value': 'automated'}]}
        ]
    )[0]
    info('Waiting for server to launch')
    instance.wait_until_running()
    success('Server created')

    context.instance = instance

def bootstrap(context):
    """
    Run bootstrap.sh to launch the initial services. Collect metadata about the launched services from
    stdout of the process.
    """

    template = context.env.get_template('bootstrap.sh.j2')
    script = template.render(context.template_payload())

    command = [
        'ssh',
        '-i', os.path.join('secrets', 'id_rsa'),
        'core@{}',
        '/bin/bash'
    ]
    pipe = Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = pipe.communicate(
        script,
        timeout=context.config.getint('bootstrap', 'timeout')
    )

    if pipe.returncode == 0:
        # Parse container metadata from stdout
    else:
        # Raise an exception with errs

def report_success(context):
    """
    Report a successful launch to the Slack webhook.
    """

def report_failure(context, e):
    """
    Report a failed launch to the Slack webhook.
    """

def cleanup(context):
    """
    Delete any and all resources provisioned during this execution.
    """

def main():
    """
    Entrypoint for the provisioner.
    """

    context = Context()
    try:
        ssh_key(context)
        server(context)
        bootstrap(context)
        report_success(context)
    except e:
        report_failure(context, e)
        cleanup(context)
