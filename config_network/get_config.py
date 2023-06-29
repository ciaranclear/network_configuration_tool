"""
* gets the configuration file.
* colates global and interface data.
* returns a formatted config with connection, global and interfaces data.
"""

def get_global_string(config_str, config_data):

    # get global lines
    try:
        lines = config_data["global"]
    except KeyError:
        pass
    else:
        for line in lines:
            config_str += f"{line}\n"

    # get global lines for each protocol
    for k, v in config_data.items():
        if k != "global":
            try:
                lines = config_data[k]["global"]
            except KeyError:
                pass
            else:
                for line in lines:
                    config_str += f"{line}\n"

    return config_str

def get_interfaces_string(config_str, config_data):

    interfaces_dict = {}

    # get interfaces lines
    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]

        for iface_name, interface in interfaces.items():
            interfaces_dict[iface_name] = interface

    # get interfaces lines for each protocol
    for k, v in config_data.items():
        if k not in ["global","interfaces","connection_data"]:
            if "interfaces" in v.keys():
                interfaces = v["interfaces"]
                for iface_name, lines in interfaces.items():
                    interfaces_dict[iface_name]["lines"] = lines

    # concat interfaces config string
    for iface_name, interface in interfaces_dict.items():
        iface_type = interface["iface_type"]
        iface_id = interface["iface_id"]
        lines = interface["lines"]
        if lines:
            lines = list(set(lines))
            config_str += f"interface {iface_type} {iface_id}\n"
            for line in lines:
                config_str += f"{line}\n"
            config_str += "exit\n"
            
    return config_str

def get_config_string(config_data):

    config_str = ""

    config_str = get_global_string(config_str, config_data)
    config_str = get_interfaces_string(config_str, config_data)

    return config_str
