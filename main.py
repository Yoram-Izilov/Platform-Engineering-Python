import argparse
import argcomplete
from argparse import RawTextHelpFormatter
from ec2 import ec2_handler
from s3 import s3_handler
from route53 import create_private_hosted_zone, manage_dns_records

parser = argparse.ArgumentParser(description='Creates AWS resources.', formatter_class=RawTextHelpFormatter)

# Subparsers for each resource type (ec2, s3, route53)
subparsers = parser.add_subparsers(dest='resource', required=True)

# EC2 specific arguments
ec2_parser = subparsers.add_parser('ec2', help='EC2 related options')
ec2_parser.add_argument('--action',
                        type=lambda s: s.lower(), 
                        required=True,
                        choices=['create', 'manage', 'list'],
                        default='create',   
                        help='create - creates a new EC2 instance\n' +
                             'manage - start or stops \n list EC2 instances (default creates)')
ec2_parser.add_argument('--os',
                        type=lambda s: s.lower(), 
                        choices=['ubuntu', 'amazon'],
                        default='ubuntu',
                        help='AWS AMI - ubuntu or amazon (default ubuntu)')
ec2_parser.add_argument('--instance-type',
                        type=lambda s: s.lower(), 
                        choices=['t2', 't3'],
                        default='t2',
                        help='instance type - t2 or t3 (t2.micro or t3.nano)')
ec2_parser.add_argument('--instance-id',
                        type=lambda s: s.lower(), 
                        help='The id of the instance')
ec2_parser.add_argument('--state',
                        type=lambda s: s.lower(), 
                        choices=['start', 'stop', 'terminate'],
                        default='start',
                        help='Instanse state - start, stop or terminate (default start)')


# S3 specific arguments
s3_parser = subparsers.add_parser('s3', help='S3 related operations')
s3_parser.add_argument('--action',
                        type=lambda s: s.lower(), 
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
                        type=lambda s: s.lower(), 
                        choices=['public', 'private'],
                        default='private',
                        help='Bucket access type - public or private (default private)')

# Create hosted zone
create_zone_parser = subparsers.add_parser('r53-create-zone', help='Create a new DNS hosted zone')
create_zone_parser.add_argument('--zone-name',
                                type=str,
                                required=True,
                                help='Name of the DNS zone to create')
# Manage DNS records
manage_records_parser = subparsers.add_parser('r53-manage-records', help='Manage DNS records in a zone')
manage_records_parser.add_argument('--zone-id',
                                    type=str,
                                    required=True,
                                    help='ID of the DNS zone')
manage_records_parser.add_argument('--action',
                                    type=lambda s: s.lower(), 
                                    required=True,
                                    choices=['create', 'upsert', 'delete'],
                                    help='Action to perform on the record')
manage_records_parser.add_argument('--record-name',
                                    type=str,
                                    required=True,
                                    help='Name of the DNS record')
manage_records_parser.add_argument('--record-type',
                                    type=lambda s: s.upper(), 
                                    required=True,
                                    choices=['A', 'CNAME', 'TXT', 'MX'],
                                    help='Type of the DNS record')
manage_records_parser.add_argument('--record-value',
                                    type=str,
                                    required=True,
                                    help='Value of the DNS record')

# Enable autocomplete
argcomplete.autocomplete(parser)
# Parse the arguments
args = parser.parse_args() 

match args.resource:
    case "ec2":
        ec2_handler(args.action, args.os, args.instance_type,
                    args.instance_id if args.instance_id else None, args.state)
    case "s3":
        if args.bucket_name or args.action == 'list':
            s3_handler(args.action, args.bucket_name if args.bucket_name else None,
                       args.file if args.file else None, args.access)
        else:
            print("You have to add bucket name when using create and upload action. see help 's3 -h'")
    case "r53-create-zone":
        create_private_hosted_zone(args.zone_name)
    case "r53-manage-records":
        print(args.action.upper())
        manage_dns_records(args.zone_id, args.action, args.record_name, args.record_type, args.record_value)

  