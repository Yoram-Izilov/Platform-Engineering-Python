import boto3
from consts import EC2_Settings, Tag

# Creates ec2 session using aws cli
ec2_resource = boto3.resource('ec2', region_name='us-east-1')

def ec2_handler(action: str, os: str, instance_type: str, instance_id, command: str):
    """Handles EC2 actions based on the action value.
     
    :param str action: The action to perform ('create', 'manage', 'list')
    :param str os: Operating system for the EC2 instance ('ubuntu' or 'amazon')
    :param str instance_type: Type of the EC2 instance ('t2' or 't3')
    :param instance_id: str or None - ID of the EC2 instance (required if action is 'manage')
    :param str state: Desired state for the instance ('start', 'stop', 'terminate')
    """
    match action:
        case "create":
            create_instances(os, instance_type)
        case "manage":
            manage_instance(instance_id, command)
        case "list":
            list_instances()

def create_instances(os: str, instance_type: str):
    """Creates a new EC2 instance with the specified OS and instance type.
    
    :param str os: Operating system for the EC2 instance ('ubuntu' or 'amazon')
    :param str instance_type: Type of the EC2 instance ('t2' or 't3')
    """
    print('creates ec2 with the following params:', os, instance_type)

    if(count_running_instances() >= 2):
        print('You have 2 instances running,\n' + 'You are not allowed to open another one')
        return
    # Launch the EC2 instance
    instance = ec2_resource.create_instances(
        ImageId = EC2_Settings[os].value,  # ubuntu or amazon linux
        MinCount = 1,
        MaxCount = 1,
        InstanceType = EC2_Settings[instance_type].value, # t2 or t3 instance type
        KeyName = EC2_Settings.PEM_KEY.value,
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'SubnetId' : EC2_Settings.SUBNET_ID.value,  # Yoram-VPC-public-1 subnet
            'Groups': [
                EC2_Settings.SECURITY_GROUP.value,  # Yoram ssh all SG ID
            ],
            'AssociatePublicIpAddress': True
        }],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{
                            'Key': 'Name',
                            'Value': EC2_Settings[os].name + ' ' + Tag.TAG_VALUE.value
                        },
                        {
                            'Key': Tag.TAG_KEY.value,
                            'Value': Tag.TAG_VALUE.value
                    } 
                ]
            }
        ],
    )
    # Shows the instace id which was created
    instance_id = instance[0].id
    print(f'Launched EC2 instance with ID: {instance_id}')

def count_running_instances ():
    """Counts the number of running instances of the user created by this cli.

    :Returns: Number of running instances of the user created by this cli"""
    # Filter instances based on the specified tag and state
    filters = [
        {
            'Name': 'tag:{}'.format(Tag.TAG_KEY.value),
            'Values': [Tag.TAG_VALUE.value]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
    # Retrieve the instances
    instances = ec2_resource.instances.filter(Filters=filters)
    # Count the instances
    count = len(list(instances))
    return count

def list_instances():
    """Prints all instances of the user made by this cli."""
    # Filter instances based on the specified tag
    filters = [
        {
            'Name': 'tag:{}'.format(Tag.TAG_KEY.value),
            'Values': [Tag.TAG_VALUE.value]
        }
    ]
    # Retrieve the instances
    instances = ec2_resource.instances.filter(Filters=filters)
    # List the instances
    instance_list = []
    for instance in instances:   
        instance_info = {
            'Instance ID': instance.id,
            'Instance Type': instance.instance_type,
            'State': instance.state['Name'],
            'Public IP': instance.public_ip_address,
            'Private IP': instance.private_ip_address
        }
        instance_list.append(instance_info)

    # Prints the instances
    if instance_list:
        print("Instances with tag '{}: {}':".format(Tag.TAG_KEY.value, Tag.TAG_VALUE.value))
        for instance in instance_list:
            print(instance)
    else:
        print(f"No instances found with tag {Tag.TAG_KEY.value}: {Tag.TAG_VALUE.value}.")

def manage_instance(instance_id: str, state: str):
    """Manages (start, stop, or terminate) an EC2 instance by its ID.

    :param str instance_id: The ID of the instance to manage
    :param str state: Desired state for the instance ('start', 'stop', 'terminate')
    """
    # Filter instances by the specified tag key and value
    filters = [
        {
            'Name': 'tag:{}'.format(Tag.TAG_KEY.value),
            'Values': [Tag.TAG_VALUE.value]
        }
    ]
    
    # Retrieve instances that match the filters
    instances = ec2_resource.instances.filter(Filters=filters)

    # Check if the specific instance_id is in the filtered instances
    for instance in instances:
        if instance.id == instance_id:
            match state:
                case "start":
                    ec2_resource.instances.filter(InstanceIds=[instance_id]).start()
                    print(f'Starting instance: {instance_id}')
                case "stop":
                    ec2_resource.instances.filter(InstanceIds=[instance_id]).stop()
                    print(f'Stopping instance: {instance_id}')
                case "terminate":
                    ec2_resource.instances.filter(InstanceIds=[instance_id]).terminate()
                    print(f'Terminating instance: {instance_id}')
            return

    print("Invalid instace id. list instances to know what instance ids you have")