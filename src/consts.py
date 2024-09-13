from enum import Enum
import socket

hostname = ''
def set_hostname(args_hostname=None):
    global hostname 
    if args_hostname != '' and args_hostname:
        hostname = args_hostname
    else:
        hostname = socket.gethostname()

def get_hostname():
    return hostname

# all the consts will be in this file (ami and such)
class EC2_Settings(Enum):
    UBUNTU = 'ami-0182f373e66f89c85'
    AMAZON = 'ami-0e86e20dae9224db8'
    T2 = 't2.micro'
    T3 = 't3.nano'
    SUBNET_ID = 'subnet-0452b44b8cc2a5a34'
    SECURITY_GROUP = 'sg-02a922a216b8f2690'
    PEM_KEY = 'yoram-key-home'

# s3 Tag
class Tag(Enum):
    TAG_KEY = 'python-ID'   
    # TAG_VALUE = get_hostname()

# Route53 identifiers
class Route(Enum):
    VPC_ID = 'vpc-0d389958a2c0cadd0'
    # HOSTNAME = get_hostname()

