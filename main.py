import argparse
from argparse import RawTextHelpFormatter
from ec2 import ec2_handler

parser = argparse.ArgumentParser(description='Creates AWS resources.' ,formatter_class=RawTextHelpFormatter)
parser.add_argument('--resource',
                     type=str,
                     required=True,
                     help='Specify the AWS resource (EC2, S3, ROUTE53)')
parser.add_argument('--action',
                     type=str,
                     default='create',
                     help='create, update, delete or list the resource (default creates)')
parser.add_argument('--os',
                    type=str,
                    default='ubuntu',
                    help='Specify the AWS AMI [ubuntu, amazon] (default ubuntu)')
parser.add_argument('--machine',
                    type=str,
                    default='t2',
                    help='values t3 or t2 (t3.nano or t2.micro)')

# Parse the arguments
args = parser.parse_args()

if args.resource.upper() == "EC2":
    print("You have selected EC2 as the resource.")
    ec2_handler(args.action, args.os, args.machine)
else:
    print(f"Resource {args.resource} is not recognized.")

