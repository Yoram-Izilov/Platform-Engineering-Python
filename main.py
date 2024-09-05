import argparse
from ec2 import ec2_handler

parser = argparse.ArgumentParser(description='Creates AWS resources.')
parser.add_argument('--resource',
                     type=str,
                     required=True,
                     help='Specify the AWS resource (EC2)')
parser.add_argument('--action',
                     type=str,
                     default='create',
                     help='create, update or delete the EC2 (default creates)')
parser.add_argument('--os',
                    type=str,
                    default='ubuntu',
                    help='Specify the AWS AMI [ubuntu, amazon] (default ubuntu)')
parser.add_argument('--machine',
                    type=str,
                    default='t2.micro',
                    help='t3.nano or t2.micro (default t2.micro)')

# Parse the arguments
args = parser.parse_args()

# Access and use the --resource argument
if args.resource.upper() == "EC2":
    print("You have selected EC2 as the resource.")
    ec2_handler(args.action, args.os, args.machine)
else:
    print(f"Resource {args.resource} is not recognized.")

