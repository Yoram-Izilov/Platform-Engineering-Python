import argparse
from ec2 import create_ec2, update_ec2, list_ec2

parser = argparse.ArgumentParser(description='Creates AWS resources.')
parser.add_argument('--resource',
                     type=str,
                     required=True,
                     help='Specify the AWS resource (ec2)')
parser.add_argument('--linux',
                    type=str,
                    default='ubuntu',
                    help='Specify the AWS AMI (ubuntu, amazon)')

# Parse the arguments
args = parser.parse_args()

# Access and use the --resource argument
if args.resource == "ec2":
    print("You have selected EC2 as the resource.")
    
else:
    print(f"Resource {args.resource} is not recognized.")

