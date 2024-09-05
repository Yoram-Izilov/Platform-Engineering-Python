from enum import Enum
import socket

def get_hostname():
    hostname = socket.gethostname()
    return hostname

# all the consts will be in this file (ami and such)
class EC2_Settings(Enum):
    ubuntu = 'ami-0182f373e66f89c85'
    amazon = 'ami-0e86e20dae9224db8'
    t2 = 't2.micro'
    t3 = 't3.nano'
    SubnetId = 'subnet-0452b44b8cc2a5a34'
    SecurityGroup = 'sg-02a922a216b8f2690'
    Key = 'python-ID'
    Value = get_hostname()
    Pem_Key = 'yoram-key-home'