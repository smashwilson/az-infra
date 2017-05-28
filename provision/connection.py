import boto3

ec2 = boto3.resource('ec2')
elb = boto3.client('elb')
