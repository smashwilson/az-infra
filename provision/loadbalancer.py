from botocore.exceptions import ClientError

from provision.connection import elb, ec2
from provision.output import info, success, error

def provision(context):
    """
    Provision an elastic load balancer if necessary. Collect existing instance targets.
    """

    if not existing_loadbalancer(context):
        security_group(context)
        create_loadbalancer(context)

def security_group(context):
    """
    Create a security group to attach to the load balancer.
    """

    security_group_name = context.make_name('elb_firewall')
    info('creating ELB security group {}', security_group_name)
    context.elb_security_group = ec2.create_security_group(
        GroupName=security_group_name,
        Description='Inbound ELB traffic'
    )
    info('authorizing HTTPS and HTTP traffic')
    for port in [80, 443]:
        context.elb_security_group.authorize_ingress(
            IpProtocol='tcp',
            FromPort=port,
            ToPort=port,
            CidrIp='0.0.0.0/0'
        )
    success('ELB security group {} created', security_group_name)

def existing_loadbalancer(context):
    """
    Gather information about an existing load balancer, if one is present.
    """

    try:
        existing = elb.describe_load_balancers(
            LoadBalancerNames=[context.config.loadbalancer_name],
        )['LoadBalancerDescriptions']
        if existing:
            loadbalancer = existing[0]
            info('discovered existing load balancer {}', context.config.loadbalancer_name)
            context.elb_targets = []
            for instance in loadbalancer['Instances']:
                context.elb_targets.append({
                    'InstanceId': instance['InstanceId'],
                    'IpAddr': ec2.Instance(instance['InstanceId']).public_ip_address
                })
            return True
        else:
            return False
    except ClientError:
        return False


def create_loadbalancer(context):
    """
    Create a new load balancer.
    """

    info('creating load balancer {}', context.config.loadbalancer_name)
    elb.create_load_balancer(
        LoadBalancerName=context.config.loadbalancer_name,
        Listeners=[
            {
                'Protocol': 'tcp',
                'LoadBalancerPort': 443,
                'InstanceProtocol': 'tcp',
                'InstancePort': 443
            },
            {
                'Protocol': 'tcp',
                'LoadBalancerPort': 80,
                'InstanceProtocol': 'tcp',
                'InstancePort': 80
            }
        ],
        AvailabilityZones=[context.config.instance_az],
        SecurityGroups=[context.elb_security_group.id],
        Tags=context.make_tags()
    )
    success('load balancer {} created', context.config.loadbalancer_name)

    context.elb_targets = []
