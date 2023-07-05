from netmiko import ConnectHandler


def get_initial_configs(conn_data, commands):

    with ConnectHandler(ip = conn_data["ip_address"],
                        port = conn_data["port"],
                        username = conn_data["username"],
                        password = conn_data["password"],
                        secret = conn_data["secret"],
                        device_type = conn_data["device_type"]) as ch:
        ch.enable()

        initial_configs = {}

        for command in commands:
            try:
                output = ch.send_command(f"show {command}")
                output += '\n'
            except Exception as e:
                output = None
            initial_configs[command] = output

        return initial_configs