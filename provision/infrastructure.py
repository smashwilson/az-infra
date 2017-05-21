import os
import sys
import configparser
import subprocess
import socket
import shutil
import traceback
from .output import info, success, error

import boto3
from jinja2 import Environment, FileSystemLoader

def mustache(text):
    """
    Jinja2 filter to wrap text in verbatim {{ }}.
    """

    return "{{ {} }}".format(text)

class Context:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.build_no = os.environ.get('TRAVIS_JOB_NUMBER', '0')

        self.ec2 = boto3.resource('ec2', region_name=self.config.get('server', 'region'))

        loader = FileSystemLoader(
            os.path.join(os.path.dirname(__file__), '..', 'template')
        )
        self.env = Environment(
            loader=loader,
            autoescape=False,
            auto_reload=False
        )
        self.env.filters['mustache'] = mustache

        self.key_pair = None
        self.sg = None
        self.instance = None

    def make_name(self, base):
        return base + '_' + self.build_no

    def template_payload(self):
        return {
            'pushbot': {
                'branch': 'k8s-and-postgres',
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
    shutil.copyfile(os.path.join('secrets', 'id_rsa'), os.path.join('out', 'id_rsa'))
    success('SSH key generated')

    info('Uploading SSH key to AWS')
    context.key_pair = context.ec2.import_key_pair(
        KeyName=context.make_name('key'),
        PublicKeyMaterial=pub_key_material
    )
    success('SSH key {} uploaded'.format(context.key_pair.key_name))

def server(context):
    """
    Launch a CoreOS server.
    """

    security_group_name = context.make_name('firewall')
    info('Creating security group {}'.format(security_group_name))
    sg = context.ec2.create_security_group(
        GroupName=security_group_name,
        Description='Permit SSH access',
    )
    context.sg = sg
    info('Authorizing SSH access')
    sg.authorize_ingress(
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        CidrIp='0.0.0.0/0',
    )

    info('Creating server')
    instance = context.ec2.create_instances(
        ImageId=context.config.get('server', 'image_id'),
        MinCount=1,
        MaxCount=1,
        KeyName=context.key_pair.key_name,
        SecurityGroups=[security_group_name],
        InstanceType=context.config.get('server', 'instance_type'),
        TagSpecifications=[
            {'ResourceType': 'instance', 'Tags': [{'Key': 'creation', 'Value': 'automated'}]}
        ]
    )[0]
    context.instance = instance

    info('Waiting for server {} to launch'.format(context.instance.id))
    context.instance.wait_until_running()
    context.instance.reload()
    success('Server {} created and running at {}'.format(context.instance.id, context.instance.public_ip_address))

    info('Waiting for port 22 to begin listening at {}'.format(context.instance.public_ip_address))
    for i in range(60):
        try:
            s = socket.create_connection((context.instance.public_ip_address, 22), 10)
        except:
            pass
        else:
            success('Port 22 is alive.')
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return
    raise RuntimeError('Timed out waiting for SSH daemon.')


def bootstrap(context):
    """
    Run bootstrap.sh to launch the initial services. Collect metadata about the launched services from
    stdout of the process.
    """

    keyscan = subprocess.run(
        ['ssh-keyscan', context.instance.public_ip_address],
        check=True,
        stdout=subprocess.PIPE,
        encoding='utf-8',
        universal_newlines=False
    )

    os.makedirs(os.path.join(os.environ['HOME'], '.ssh'), mode=0o700, exist_ok=True)
    with open(os.path.join(os.environ['HOME'], '.ssh', 'known_hosts'), 'w') as hostfile:
        hostfile.write(keyscan.stdout)

    template = context.env.get_template('bootstrap.sh.j2')
    script = template.render(context.template_payload())
    # print('script:\n{}'.format(script), flush=True)

    command = [
        'ssh',
        '-i', os.path.join('secrets', 'id_rsa'),
        'core@{}'.format(context.instance.public_ip_address),
        '/bin/bash'
    ]
    info('Bootstrapping server {}'.format(context.instance.id))
    pipe = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
        universal_newlines=False
    )
    outs, errs = pipe.communicate(
        script,
        timeout=context.config.getint('bootstrap', 'timeout')
    )

    print('status:\n{}'.format(pipe.returncode))
    print('stdout:\n{}'.format(outs))
    print('stderr:\n{}'.format(errs))

    if pipe.returncode == 0:
        # Parse container metadata from stdout
        pass
    else:
        # Raise an exception with errs
        pass
    # raise RuntimeError('tear it down')

def report_success(context):
    """
    Report a successful launch to the Slack webhook.
    """

    success('Success')

def report_failure(context):
    """
    Report a failed launch to the Slack webhook.
    """

    error('Failure: {}'.format(traceback.format_exc()))

def cleanup(context):
    """
    Delete any and all resources provisioned during this execution.
    """

    if context.key_pair:
        context.key_pair.delete()
        success('key pair deleted.')
    if context.instance:
        info('terminating instance.')
        context.instance.terminate()
        context.instance.wait_until_terminated()
        success('instance terminated.')
    if context.sg:
        context.sg.delete()
        success('security group deleted.')

def report_cleanup(context):
    """
    Report that everything was cleaned up correctly after a build failure.
    """

    success('All resources cleaned.')

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
    except:
        report_failure(context)
        cleanup(context)
        report_cleanup(context)
