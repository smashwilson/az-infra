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

    if context.instance:
        try:
            info('revoking RDS security group ingress rule')
            rds_security_group = ec2.SecurityGroup(context.config.rds_security_group_id)
            rds_security_group.revoke_ingress(
                IpProtocol='tcp',
                FromPort=5432,
                ToPort=5432,
                CidrIp='{}/32'.format(context.instance.public_ip_address),
            )
            info('RDS security group ingress rule revoked')
        except:
            had_failure = True
            error('unable to remove RDS security group rule\n{}'.format(traceback.format_exc()))

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

    pushbot_instances = ec2.instances.filter(
        Filters=[
            {'Name': 'tag:purpose', 'Values': ['pushbot']},
            {'Name': 'instance-state-name', 'Values': ['pending', 'running']}
        ]
    )
    pushbot_security_groups = ec2.security_groups.filter(
        Filters=[{'Name': 'tag:purpose', 'Values': ['pushbot']}]
    )
    pushbot_key_pairs = ec2.key_pairs.filter(
        Filters=[{'Name': 'key-name', 'Values': ['pushbot*']}]
    )

    rds_security_group = ec2.SecurityGroup(context.config.rds_security_group_id)
    pushbot_rds_rules = rds_security_group.ip_permissions

    prior_instances = [i for i in pushbot_instances if i.id != context.instance.id]
    prior_security_groups = [g for g in pushbot_security_groups if g.id != context.security_group.id]
    prior_key_pairs = [k for k in pushbot_key_pairs if k.name != context.key_pair.name]

    prior_rds_rules = []
    for r in pushbot_rds_rules:
        ip_protocol = r['IpProtocol']
        from_port = r['FromPort']
        to_port = r['ToPort']
        for ip_range in r['IpRanges']:
            if ip_range['CidrIp'] != context.instance.public_ip_address + '/32':
                prior_rds_rules.append({
                    'IpProtocol': ip_protocol,
                    'FromPort': from_port,
                    'ToPort': to_port,
                    'CidrIp': ip_range['CidrIp']
                })

    def plural(noun, list):
        if len(list) == 1:
            return '1 ' + noun
        else:
            return '{} {}s'.format(len(list), noun)

    info('deleting ' + plural('prior key pair', prior_key_pairs))
    for k in prior_key_pairs:
        try:
            k.delete()
        except:
            had_failure = True
            error('unable to delete key pair\n{}'.format(traceback.format_exc()))

    info('revoking ' + plural('RDS security ingress rule', prior_rds_rules))
    for r in prior_rds_rules:
        try:
            rds_security_group.revoke_ingress(**r)
        except:
            had_failure = True
            error('unable to revoke RDS ingress rule\n{}'.format(traceback.format_exc()))

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
