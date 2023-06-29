"""
* takes a configuration with connection, global and interfaces data.
* performs the actual configuration of the device.
* returns the output from the device configuration.
"""
from netmiko import ConnectHandler


def config_device(conn_data, config_string):

    # connect to device and send configuraion string
    with ConnectHandler(ip = conn_data["ip_address"],
                        port = conn_data["port"],
                        username = conn_data["username"],
                        password = conn_data["password"],
                        secret = conn_data["secret"],
                        device_type = conn_data["device_type"]) as ch:

        config_set = config_string.split("\n")
        output = ch.send_config_set(config_set)
        return output
