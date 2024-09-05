import argparse
from argparse import RawTextHelpFormatter
from ec2 import ec2_handler

parser = argparse.ArgumentParser(description='Creates AWS resources.', formatter_class=RawTextHelpFormatter)

# Subparsers for each resource type (ec2, s3, route53)
subparsers = parser.add_subparsers(dest='resource', required=True)

# EC2 specific arguments
ec2_parser = subparsers.add_parser('ec2', help='EC2 related options')
ec2_parser.add_argument('--action',
                        type=str,
                        default='create',
                        choices=['create', 'update', 'list'],
                        help='create, update or list the resource (default creates)')
ec2_parser.add_argument('--os',
                        type=str,
                        default='ubuntu',
                        choices=['ubuntu', 'amazon'],
                        help='AWS AMI - ubuntu or amazon (default ubuntu)')
ec2_parser.add_argument('--instance',
                        type=str,
                        default='t2',
                        choices=['t2', 't3'],
                        help='instance type - t2 or t3 (t2.micro or t3.nano)')

# S3 specific arguments
s3_parser = subparsers.add_parser('s3', help='S3 related options')
# Add S3 specific arguments here

# Route53 specific arguments
route53_parser = subparsers.add_parser('route53', help='Route53 related options')
# Add Route53 specific arguments here

# Parse the arguments
args = parser.parse_args() 

# Match on the resource type
match args.resource:
    case "ec2":
        print("You have selected EC2 as the resource.")
        ec2_handler(args.action.lower(), args.os.lower(), args.instance.lower())
    case "s3":
        print("You have selected S3 as the resource.")
    case "route53":
        print("You have selected Route53 as the resource.")
    case _:
        print(f"Resource {args.resource} is not recognized.")