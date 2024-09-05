from enum import Enum

# all the consts will be in this file (ami and such)
class AMI(Enum):
    ubuntu = 'ami-0182f373e66f89c85'
    amazon = 'ami-0e86e20dae9224db8'

class Instance_Type(Enum):
    t2 = 't2.micro'
    t3 = 't3.nano'