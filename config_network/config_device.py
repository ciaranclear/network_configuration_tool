"""
* takes a configuration with connection, global and interfaces data.
* performs the actual configuration of the device.
* returns the output from the device configuration.
* check % does not appear at the beggining of any line in the output.
"""
from netmiko import ConnectHandler
import time

def config_device(conn_data, config_string):

    config_set = config_string.split("\n")
    output = None

    with ConnectHandler(ip = conn_data["ip_address"],
                        port = conn_data["port"],
                        username = conn_data["username"],
                        password = conn_data["password"],
                        secret = conn_data["secret"],
                        fast_cli = False,
                        read_timeout_override = 60,
                        conn_timeout = 20,
                        device_type = conn_data["device_type"]) as ch:
        output = ch.send_config_set(config_set)
        ch.cleanup()
        ch.disconnect()

    return output