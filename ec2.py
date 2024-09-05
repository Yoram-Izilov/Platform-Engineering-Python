import boto3
from consts import EC2_Settings, get_hostname

# Creates ec2 session using aws cli
ec2_resource = boto3.resource('ec2', region_name='us-east-1')

def ec2_handler(action, os, instance_type):
    print(get_hostname())
    match action.lower():
        case "create":
            create_ec2(os, instance_type)
        case "manage":
            update_ec2(os, instance_type)
        case "list":
            list_ec2()
        case _:
            print('please see the help section to know what is possible with the EC2 resource')

def create_ec2(os, instance_type):
    print('creates ec2 with the following params:', os, instance_type)

    if(count_running_EC2() >= 2):
        print('You have 2 instances running,\n' + 'You are not allowed to open another one')
        return
    # Launch the EC2 instance
    instance = ec2_resource.create_instances(
        ImageId = EC2_Settings[os].value,  # ubuntu or amazon linux
        MinCount=1,
        MaxCount=1,
        InstanceType= EC2_Settings[instance_type].value, # t2 or t3 instance type
        KeyName='yoram-key-home',
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'SubnetId' : EC2_Settings['SubnetId'].value,  # Yoram-VPC-public-1 subnet
            'Groups': [
                EC2_Settings['SecurityGroup'].value,  # Yoram ssh all SG ID
            ],
            'AssociatePublicIpAddress': True
        }],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{
                        'Key': 'Name',
                        'Value': EC2_Settings[os].name + EC2_Settings['Value'].value
                    },{
                        'Key': EC2_Settings['Key'].value,
                        'Value': EC2_Settings['Value'].value
                    } 
                ]
            }
        ],
    )
    # Shows the instace id which was created
    instance_id = instance[0].id
    print(f'Launched EC2 instance with ID: {instance_id}')

def count_running_EC2 ():
    # Filter instances based on the specified tag and state
    filters = [
        {
            'Name': 'tag:{}'.format(EC2_Settings['Key'].value),
            'Values': [EC2_Settings['Value'].value]
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

def list_ec2():
    # Filter instances based on the specified tag
    filters = [
        {
            'Name': 'tag:{}'.format(EC2_Settings['Key'].value),
            'Values': [EC2_Settings['Value'].value]
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
        print("Instances with tag '{}: {}':".format(EC2_Settings['Key'].value, EC2_Settings['Value'].value))
        for instance in instance_list:
            print(instance)
    else:
        print(f"No instances found with tag {EC2_Settings['Key'].value}: {EC2_Settings['Value'].value}.")

def update_ec2(os, instance_type):
    pass