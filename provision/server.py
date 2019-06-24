import os
import pathlib
import shutil
import socket
import subprocess
import time
import json
import re
import urllib.request

from provision import template
from provision.connection import ec2, client
from provision.output import info, success, error

def provision(context):
    """
    Provision and bootstrap a CoreOS server.
    """

    ssh_key(context)
    security_group(context)
    instance(context)
    bootstrap(context)
    bind_elastic_ip(context)

def ssh_key(context):
    """
    Create a new SSH key and upload it to EC2.
    """

    info('generating SSH key')
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
    if pathlib.Path('out').is_dir():
        shutil.copyfile(os.path.join('secrets', 'id_rsa'), os.path.join('out', 'id_rsa'))
    success('SSH key generated')

    info('importing SSH key to EC2')
    context.key_pair = ec2.import_key_pair(
        KeyName=context.make_name('key'),
        PublicKeyMaterial=pub_key_material
    )
    success('SSH keypair {} uploaded to EC2'.format(context.key_pair.key_name))

def security_group(context):
    """
    Create a new security group to associate with the instance.
    """

    security_group_name = context.make_name('firewall')
    info('creating security group {}'.format(security_group_name))
    context.security_group = ec2.create_security_group(
        GroupName=security_group_name,
        Description='Azurefire host firewall',
    )

    context.security_group.create_tags(Tags=context.make_tags())
    info('authorizing SSH, HTTP and HTTPS access to nginx and az-coordinator')
    for port in [22, 80, 443, 8443]:
        context.security_group.authorize_ingress(
            IpProtocol='tcp',
            FromPort=port,
            ToPort=port,
            CidrIp='0.0.0.0/0',
        )
    success('security group {} created'.format(security_group_name))

def instance(context):
    """
    Run a new EC2 instance. Return when it has booted successfully and is listening on port 22.
    """

    info('creating instance')
    context.instance = ec2.create_instances(
        ImageId=context.config.server_image_id,
        MinCount=1,
        MaxCount=1,
        KeyName=context.key_pair.key_name,
        SecurityGroups=[context.security_group.group_name],
        InstanceType=context.config.server_instance_type,
        IamInstanceProfile={'Arn': context.config.server_instance_profile_arn},
        Placement={'AvailabilityZone': context.config.server_instance_az},
        TagSpecifications=[
            {'ResourceType': 'instance', 'Tags': context.make_tags()}
        ]
    )[0]

    info('waiting for instance {} to launch'.format(context.instance.id))
    context.instance.wait_until_running();
    context.instance.reload()

    info('authorizing traffic to RDS security group {}'.format(context.config.rds_security_group_id))
    rds_security_group = ec2.SecurityGroup(context.config.rds_security_group_id)
    rds_security_group.authorize_ingress(
        IpProtocol='tcp',
        FromPort=5432,
        ToPort=5432,
        CidrIp='{}/32'.format(context.instance.public_ip_address),
    )

    info('waiting for instance {} to listen on port 22'.format(context.instance.id))
    _wait_for_ssh(context.instance.public_ip_address, context.config.server_ssh_timeout)
    success('instance {} has booted and is listening at {}:22'.format(
        context.instance.id, context.instance.public_ip_address))

def bootstrap(context):
    """
    Connect to the EC2 instance over SSH and pipe the bootstrapping script to bash.
    """

    info('locating the download URL for the latest az-coordinator release')

    az_coordinator_download_url = None
    req = urllib.request.Request(
        url='https://api.github.com/repos/smashwilson/az-coordinator/releases/latest',
        headers={
            'Accept': 'application/vnd.github.v3+json',
            'User-agent': 'smashwilson az-infra'
        }
    )
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
        for asset in body['assets']:
            if re.match(r'.*linux_amd64\.tar\.gz$', asset['name']):
                context.az_coordinator_download_url = asset['browser_download_url']
    if not context.az_coordinator_download_url:
        raise RuntimeError("Unable to find a Linux binary in the latest az-coordinator release")

    info('generating bootstrapping script from template')
    script = template.render(context, 'bootstrap.sh.j2')

    info('executing bootstrap script')
    ssh = [
        'ssh',
        '-i', os.path.join('secrets', 'id_rsa'),
        '-o', 'StrictHostKeyChecking=no',
        'core@{}'.format(context.instance.public_ip_address),
        '/bin/bash'
    ]
    process = subprocess.run(ssh, input=script.encode('utf-8'), timeout=context.config.bootstrap_timeout)

    if process.returncode == 0:
        success('bootstrapping completed successfully')
    else:
        error('bootstrapping script failure:')
        error('exit status: {}'.format(process.returncode))
        raise RuntimeError('bootstrapping failure')

def bind_elastic_ip(context):
    """
    Associate the elastic IP with the instance.
    """

    info('associating the elastic IP with the new instance')
    client.associate_address(
        AllocationId=context.config.elastic_ip_id,
        InstanceId=context.instance.id,
        AllowReassociation=True,
    )
    success('instance is associated with the elastic IP')

def _wait_for_ssh(public_ip, attempts):
    """
    Wait for an SSH daemon to begin listening at port 22.
    """

    for i in range(120):
        try:
            s = socket.create_connection((public_ip, 22), 10)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return
        except socket.timeout:
            info('{}: timeout'.format(i))
            pass
        except ConnectionRefusedError:
            info('{}: connection refused'.format(i))
            time.sleep(5)
    raise RuntimeError('Timed out waiting for SSH daemon')
