"""
PRECEDENCE OF LINES

1. global lines.
2. protocol global lines.
3. interfaces before lines.
4. ranges before lines.
5. interfaces lines.
6. ranges lines.
7. interfaces after lines.
8. ranges after lines.

"""

def get_config_string(config_data):

    config_str = ""

    config_str += get_global_string(config_data)
    config_str += get_interfaces_string(config_data)

    return config_str

def get_global_string(config_data):
    
    global_str = ""

    if "globals" in config_data.keys():
        globals = config_data["globals"]
        for _, lines in globals.items():
            for line in lines:
                global_str += f"{line}\n"

    return global_str

def get_interfaces_string(config_data):
    
    ifaces_str = ""

    modes = [
        "before",
        None,
        "after"
    ]

    ifaces_dict = interfaces_dict(config_data)

    for _, iface_list in ifaces_dict.items():
        if iface_list:
            iface_type = iface_list[0]["iface_type"]
            iface_id = iface_list[0]["iface_id"]
            ifaces_str += f"interface {iface_type} {iface_id}\n"
            for iface_obj in iface_list:
                for mode in modes:
                    if iface_obj["mode"] == mode:
                        lines = iface_obj["lines"]
                        for line in lines:
                            ifaces_str += f"{line}\n"
            ifaces_str += "exit\n"

    return ifaces_str

def get_protocols(config_data):

    non_protocols = [
        "connection_data",
        "global",
        "interfaces"
    ]

    protocols = []

    for k in config_data.keys():
        if k not in non_protocols:
            protocols.append(k)

    return protocols

def interfaces_dict(config_data):

    ifaces = {}

    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
        for _, ifaces_dict in interfaces.items():
            for iface_name, iface_dict in ifaces_dict.items():
                if iface_name not in ifaces.keys():
                    ifaces[iface_name] = [iface_dict]
                else:
                    ifaces[iface_name].append(iface_dict)

    if "ranges" in config_data.keys():
        ranges = config_data["ranges"]
        for _, ranges_list in ranges.items():
            for range_obj in ranges_list:
                iface_name_prefix = range_obj["iface_name_prefix"]
                iface_type = range_obj["iface_type"]
                iface_ids = range_obj["iface_ids"]
                mode = range_obj["mode"]
                lines = range_obj["lines"]
                for iface_id in iface_ids:
                    obj = {
                        "iface_type":iface_type,
                        "iface_id":iface_id,
                        "mode":mode,
                        "lines":lines
                    }
                    iface_name = f"{iface_name_prefix}{iface_id}"
                    if iface_name in ifaces.keys():
                        ifaces[iface_name].append(obj)
                    else:
                        ifaces[iface_name] = [obj]

    return ifaces