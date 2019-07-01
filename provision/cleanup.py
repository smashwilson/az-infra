import traceback

from provision.connection import ec2
from provision.output import info, success, error

def rollback(context):
    """
    Delete any and all resources provisioned during this provisioning execution.
    """

    had_failure = False

    if context.key_pair:
        try:
            info('deleting key pair')
            context.key_pair.delete()
            info('key pair deleted')
        except:
            had_failure = True
            error('unable to delete key pair\n{}'.format(traceback.format_exc()))

        try:
            info('terminating instance')
            context.instance.terminate()
            context.instance.wait_until_terminated()
            info('instance terminated')
        except:
            had_failure = True
            error('unable to terminate instance\n{}'.format(traceback.format_exc()))

    if context.security_group:
        try:
            info('deleting security group')
            context.security_group.delete()
            info('security group deleted')
        except:
            had_failure = True
            error('unable to delete security group\n{}'.format(traceback.format_exc()))

    if had_failure:
        error('one or more resources are still live on AWS')
    else:
        success('all resources deleted from AWS')
    return had_failure

def retire(context):
    """
    Delete any resources on the AWS account created by previous runs.
    """

    had_failure = False

    az_instances = ec2.instances.filter(
        Filters=[
            {'Name': 'tag:Purpose', 'Values': ['azinfra']},
            {'Name': 'instance-state-name', 'Values': ['pending', 'running']}
        ]
    )
    az_security_groups = ec2.security_groups.filter(
        Filters=[{'Name': 'tag:Purpose', 'Values': ['azinfra']}]
    )
    az_key_pairs = ec2.key_pairs.filter(
        Filters=[{'Name': 'key-name', 'Values': ['azurefire*']}]
    )

    if context.instance:
        prior_instances = [i for i in az_instances if i.id != context.instance.id]
    else:
        prior_instances = list(az_instances)

    if context.security_group:
        prior_security_groups = [g for g in az_security_groups if g.id != context.security_group.id]
    else:
        prior_security_groups = list(az_security_groups)

    if context.key_pair:
        prior_key_pairs = [k for k in az_key_pairs if k.name != context.key_pair.name]
    else:
        prior_key_pairs = list(az_key_pairs)

    def plural(noun, collection):
        if len(collection) == 1:
            return '1 ' + noun
        else:
            return '{} {}s'.format(len(collection), noun)

    info('deleting ' + plural('prior key pair', prior_key_pairs))
    for k in prior_key_pairs:
        try:
            k.delete()
        except:
            had_failure = True
            error('unable to delete key pair\n{}'.format(traceback.format_exc()))

    info('terminating ' + plural('prior instance', prior_instances))
    for i in prior_instances:
        try:
            i.terminate()
        except:
            had_failure = True
            error('unable to terminate instance\n{}'.format(traceback.format_exc()))
    for i in prior_instances:
        try:
            i.wait_until_terminated()
        except:
            had_failure = True
            error('unable to wait for instance to terminate\n{}'.format(traceback.format_exc()))

    info('deleting ' + plural('security group', prior_security_groups))
    for g in prior_security_groups:
        try:
            g.delete()
        except:
            had_failure = True
            error('unable to delete security group\n{}'.format(traceback.format_exc()))

    if had_failure:
        error('one or more prior resources are still live on AWS')
    else:
        success('all prior resources deleted')
    return had_failure
