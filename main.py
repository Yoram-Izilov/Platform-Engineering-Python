import argparse
from argparse import RawTextHelpFormatter
from ec2 import ec2_handler
from s3 import s3_handler

parser = argparse.ArgumentParser(description='Creates AWS resources.', formatter_class=RawTextHelpFormatter)

# Subparsers for each resource type (ec2, s3, route53)
subparsers = parser.add_subparsers(dest='resource', required=True)

# EC2 specific arguments
ec2_parser = subparsers.add_parser('ec2', help='EC2 related options')
ec2_parser.add_argument('--action',
                        type=str,
                        required=True,
                        default='create',
                        choices=['create', 'manage', 'list'],
                        help='create - creates a new EC2 instance\n' +
                             'manage - start or stops \n list EC2 instances (default creates)')
ec2_parser.add_argument('--os',
                        type=str,
                        default='ubuntu',
                        choices=['ubuntu', 'amazon'],
                        help='AWS AMI - ubuntu or amazon (default ubuntu)')
ec2_parser.add_argument('--instance-type',
                        type=str,
                        default='t2',
                        choices=['t2', 't3'],
                        help='instance type - t2 or t3 (t2.micro or t3.nano)')
ec2_parser.add_argument('--instance-id',
                        type=str,
                        help='The id of the instance')
ec2_parser.add_argument('--state',
                        type=str,
                        default='start',
                        choices=['start', 'stop', 'terminate'],
                        help='Instanse state - start, stop or terminate (default start)')


# S3 specific arguments
s3_parser = subparsers.add_parser('s3', help='S3 related operations')
s3_parser.add_argument('--action',
                       required=True,
                       choices=['create', 'upload', 'list'],
                       help='Action to perform (create, upload, list)')
s3_parser.add_argument('--bucket-name',
                       type=str,
                       help='Name of the S3 bucket')
s3_parser.add_argument('--file',
                       type=str,
                       help='File path to upload')
s3_parser.add_argument('--access',
                       type=str,
                       choices=['public', 'private'],
                       default='private',
                       help='Bucket access type - public or private (default private)')


# Route53 specific arguments
route53_parser = subparsers.add_parser('route53', help='Route53 related options')
# Add Route53 arguments 

# Parse the arguments
args = parser.parse_args() 

match args.resource:
    case "ec2":
        ec2_handler(args.action.lower(),
                    args.os.lower(),
                    args.instance_type.lower(),
                    args.instance_id.lower() if args.instance_id else None,
                    args.state.lower(),
                    )
    case "s3":
        if args.bucket_name or args.action == 'list':
            s3_handler(args.action.lower(),
                       args.bucket_name.lower() if args.bucket_name else None,
                       args.file if args.file else None,
                       args.access
                       )
        else:
            print("You have to add bucket name when using create and upload action. see help 's3 -h'")
    case "route53":
        print("You have selected Route53 as the resource.")
  