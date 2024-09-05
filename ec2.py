import boto3
from consts import AMI, Instance_Type

def ec2_handler(action: str, os: str, machine):
    match action.lower():
        case "create":
            create_ec2(os, machine)
        case "update":
            update_ec2(os, machine)
        case "delete":
            list_ec2()
        case _:
            print('please see the help section to know what is possible with the EC2 resource')

def create_ec2(os, machine):
    print('creates ec2 with the following params:', os, machine)

    # Create a session using your configured credentials
    ec2 = boto3.resource('ec2', region_name='us-east-1')

    # Launch the EC2 instance
    instance = ec2.create_instances(
        ImageId = AMI[os].value,  # ubuntu or amazon linux
        MinCount=1,
        MaxCount=1,
        InstanceType= Instance_Type[machine].value, # t2 or t3 machine
        KeyName='yoram-ssh',
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'SubnetId' : 'subnet-0452b44b8cc2a5a34',  # Yoram VPC public 1 subnet
            'Groups': [
                'sg-02a922a216b8f2690',  # Yoram ssh all SG ID
            ],
            'AssociatePublicIpAddress': True
        }],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{
                        'Key': 'Name',
                        'Value': Instance_Type[machine].value + ' Yoram'
                    },{
                        'Key': 'python-ID',
                        'Value': 'Yoram'
                    } 
                ]
            }
        ],
    )

    # Get the instance ID and other details
    instance_id = instance[0].id
    print(f'Launched EC2 instance with ID: {instance_id}')

def update_ec2(os, machine):
    pass 
def list_ec2():
    pass