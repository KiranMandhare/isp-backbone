from netmiko import ConnectHandler
import sys
from sshInfo import *

host= getHostNames()
ios_devices = fetchConnectionParameter()

i=0
for router in ios_devices:
    with ConnectHandler(**router) as connection:
        print("Comnected to "+router)
        connection.enable()
        result= connection.send_config_from_file(host[i]+".conf")
        print("Config sent to router")
        i=i+1
        print(result)
