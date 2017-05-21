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

    if context.instance and context.security_group:
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

    if context.instance:
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
