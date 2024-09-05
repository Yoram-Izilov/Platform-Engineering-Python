import boto3

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
    print('creates ec2 with the following params:')

    pass
def update_ec2(os, machine):
    pass 
def list_ec2():
    pass