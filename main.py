import argparse
from argparse import RawTextHelpFormatter
from ec2 import ec2_handler
from s3 import s3_handler
from route53 import create_private_hosted_zone, manage_dns_records
from consts import set_hostname

parser = argparse.ArgumentParser(description='Creates AWS resources.', formatter_class=RawTextHelpFormatter)
# hostname - added for jenkins pipeline by the user logged in value
parser.add_argument('--hostname', type=str, help='- creates a new running EC2 instance')

# Subparsers for each resource type (ec2, s3, route53)
subparsers = parser.add_subparsers(dest='resource', required=True)

# EC2 specific arguments
ec2_parser = subparsers.add_parser('ec2', help='EC2 related options', formatter_class=RawTextHelpFormatter)
ec2_parser.add_argument('--action',
                        type=lambda s: s.lower(), 
                        required=True,
                        choices=['create', 'manage', 'list'],
                        default='create',   
                        help=
'''create - creates a new running EC2 instance
manage - start or stops an instance
list - lists all EC2 instances 
(default value: creates)''')
ec2_parser.add_argument('--os',
                        type=lambda s: s.lower(), 
                        choices=['ubuntu', 'amazon'],
                        default='ubuntu',
                        help='AWS AMI - ubuntu or amazon operating system (default value: ubuntu)')
ec2_parser.add_argument('--instance-type',
                        type=lambda s: s.lower(), 
                        choices=['t2', 't3'],
                        default='t2',
                        help='instance type - t2 or t3 (t2.micro or t3.nano, default value: t2)')
ec2_parser.add_argument('--instance-id',
                        type=lambda s: s.lower(), 
                        help='The id of the instance - works only with the state args (action has to be = "manage")')
ec2_parser.add_argument('--state',
                        type=lambda s: s.lower(), 
                        choices=['start', 'stop', 'terminate'],
                        default='start',
                        help='Instanse state - start, stop or terminate (default value: start)')

# S3 specific arguments
s3_parser = subparsers.add_parser('s3', help='S3 related operations', formatter_class=RawTextHelpFormatter)
s3_parser.add_argument('--action',
                        type=lambda s: s.lower(), 
                        required=True,
                        choices=['create', 'upload', 'list'],
                        help='creates, uploads or lists buckets of the user')
s3_parser.add_argument('--bucket-name',
                        type=str,
                        help='Name of the user S3 bucket')
s3_parser.add_argument('--file',
                        type=str,
                        help='File path to upload')
s3_parser.add_argument('--access',
                        type=lambda s: s.lower(), 
                        choices=['public', 'private'],
                        default='private',
                        help='Bucket access type - public or private (default value: private)')

# Create hosted zone specific arguments
create_zone_parser = subparsers.add_parser('r53-create-zone', help='Create a new DNS hosted zone', formatter_class=RawTextHelpFormatter)
create_zone_parser.add_argument('--zone-name',
                                type=str,
                                required=True,
                                help='Name of the user DNS zone to create')

# Manage DNS records specific arguments
manage_records_parser = subparsers.add_parser('r53-manage-records', help='Manage DNS records in a zone', formatter_class=RawTextHelpFormatter)
manage_records_parser.add_argument('--zone-id',
                                    type=str,
                                    required=True,
                                    help='DNS zone id')
manage_records_parser.add_argument('--action',
                                    type=lambda s: s.lower(), 
                                    required=True,
                                    choices=['create', 'upsert', 'delete'],
                                    help=
'''Action to perform on the record (only if created here by the current user)
create - create a new record
upsert - updating existing record''')
manage_records_parser.add_argument('--record-name',
                                    type=str,
                                    required=True,
                                    help='DNS record name')
manage_records_parser.add_argument('--record-type',
                                    type=lambda s: s.upper(), 
                                    required=True,
                                    choices=['A', 'CNAME', 'TXT', 'MX'],
                                    help='Type of the DNS record')
manage_records_parser.add_argument('--record-value',
                                    type=str,
                                    required=True,
                                    help='Value of the DNS record')

# Parse the arguments
args = parser.parse_args() 
set_hostname(args.hostname) # for jenkins pipeline

# Match the resource type and invoke appropriate handler function
match args.resource:
    case "ec2":
        # chaning os and instance type to upper for the ENUMs
        ec2_handler(args.action, args.os.upper(), args.instance_type.upper(),
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
        manage_dns_records(args.zone_id, args.action, args.record_name, args.record_type, args.record_value)