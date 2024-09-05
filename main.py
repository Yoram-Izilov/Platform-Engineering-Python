import argparse
from argparse import RawTextHelpFormatter
from ec2 import ec2_handler

parser = argparse.ArgumentParser(description='Creates AWS resources.' ,formatter_class=RawTextHelpFormatter)
parser.add_argument('--resource',
                     type=str,
                     required=True,
                     choices=['ec2', 's3', 'route53'],
                     help='Specify the AWS resource (EC2, s3, Route53)')

# Subparsers for each resource type
subparsers = parser.add_subparsers(dest='resource', required=True)

# EC2 specific arguments
ec2_parser = subparsers.add_parser('ec2', help='EC2 related options')
ec2_parser.add_argument('--action',
                        type=str,
                        default='create',
                        help='create, update or list the resource (default creates)')
ec2_parser.add_argument('--os',
                        type=str,
                        default='ubuntu',
                        choices=['ubuntu', 'amazon'],
                        help='Specify the AWS AMI [ubuntu, amazon] (default ubuntu)')
ec2_parser.add_argument('--machine',
                        type=str,
                        default='t2',
                        choices=['t2', 't3'],
                        help='Specify machine type t2 or t3 (t2.micro or t3.nano)')
# S3 specific arguments
s3_parser = subparsers.add_parser('s3', help='S3 related options')

# Route53 specific argumentsv
route53_parser = subparsers.add_parser('route53', help='Route53 related options')

args = parser.parse_args() # parsing the args

match args.resource.lower():
    case "ec2":
        print("You have selected EC2 as the resource.")
        ec2_handler(args.action.lower(), args.os.lower(), args.machine.lower())
    case "s3":
        print("You have selected EC2 as the resource.")
        ec2_handler(args.action.lower(), args.os.lower(), args.machine.lower())
    case "route53":
        print("You have selected EC2 as the resource.")
        ec2_handler(args.action.lower(), args.os.lower(), args.machine.lower())
    case _:
        print(f"Resource {args.resource} is not recognized.")


