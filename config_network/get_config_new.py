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
from pprint import pprint

def get_config_string(config_data):
    """
    
    """
    # get global string.
    # get interfaces string.
    # concat and return string.
    validate_config(config_data)
    global_str = get_global_string(config_data)
    ifaces_str = get_interfaces_string(config_data)

    config_str = global_str + ifaces_str
    print(config_str)
    return config_str

def get_global_string(config_data):
    """
    
    """
    # get global lines.
    # get protocols global lines.
    # concat global string.
    lines = []

    lines = get_global_lines(lines, config_data)
    lines = get_protocol_global_lines(lines, config_data)

    global_str = "\n".join(lines)

    return global_str

def get_interfaces_string(config_data):
    """
    
    """
    # interfaces before lines.
    # interfaces ranges before lines.
    # protocol interfaces before lines.
    # protocol ranges before lines.
    # interfaces lines.
    # interface ranges lines.
    # protocol interfaces lines.
    # protocol ranges lines
    # interfaces after lines.
    # interfaces ranges after lines.
    # protocol interfaces after lines.
    # protocol ranges after lines.
    ifaces_dict = {}

    ifaces_str = ""

    modes = ["before", None, "after"]

    for mode in modes:
        print(f"MODE {mode}")
        #get_ifaces_lines(ifaces_dict, config_data, mode)
        get_ifaces_ranges(ifaces_dict, config_data, mode)
        get_protocol_ifaces_lines(ifaces_dict, config_data, mode)
        #get_protocol_ranges_lines(ifaces_dict, config_data, mode)

    for iface in ifaces_dict.values():
        iface_type = iface["iface_type"]
        iface_id = iface["iface_id"]
        lines = iface["lines"]

        iface_str = f"interface {iface_type} {iface_id}\n"

        for line in lines:
            iface_str += f"{line}\n"

        ifaces_str += iface_str
        
    return ifaces_str

def get_global_lines(lines, config_data):
    """
    
    """
    # get protocols.
    # if global in protocol append lines.
    if "global" in config_data.keys():
        global_lines = config_data["global"]
        for line in global_lines:
            lines.append(line)

    return lines

def get_protocols(config_data):
    """
    
    """
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

def get_protocol_global_lines(lines, config_data):
    """
    
    """
    # get protocols.
    # if global in protocol append lines.
    protocols = get_protocols(config_data)

    for protocol in protocols:
        if "global" in config_data[protocol].keys():
            global_lines = config_data[protocol]["global"]
            for line in global_lines:
                lines.append(line)

    return lines

def get_interfaces_lines(ifaces_dict, interfaces, mode):
    """
    
    """
    for iface_name, iface_dict in interfaces.items():
        if iface_name != "ranges":
            print(f"mode {mode} iface_mode {iface_dict['mode']}")
            if mode == iface_dict["mode"]:
                add_interface_entry(ifaces_dict, iface_dict, iface_name)

def get_ifaces_lines(ifaces_dict, config_data, mode):
    """
    
    """
    # if matching mode append lines.
    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
        get_interfaces_lines(ifaces_dict, interfaces, mode)

def get_protocol_ifaces_lines(ifaces_dict, config_data, mode):
    """
    
    """
    # get protocols.
    # if protocol has interfaces.
    #    if matching mode append lines.
    protocols = get_protocols(config_data)

    for protocol in protocols:
        if "interfaces" in config_data[protocol].keys():
            interfaces = config_data[protocol]["interfaces"]
            get_interfaces_lines(ifaces_dict, interfaces, mode)

def get_protocol_ranges_lines(ifaces_dict, config_data, mode):
    """
    
    """
    # get protocols.
    # if protocol has ranges in interfaces.
    #     if matching mode in ranges append lines to interfaces.
    
    protocols = get_protocols(config_data)

    for protocol in protocols:
        interfaces = None

        if "interfaces" in config_data[protocol].keys():
            interfaces = config_data[protocol]["interfaces"]

        if interfaces and "ranges" in interfaces.keys():
            ranges = interfaces["ranges"]
            for range_dict in ranges:
                if mode == range_dict["mode"]:
                    add_ranges_entry(ifaces_dict, range_dict)

def get_ifaces_ranges(ifaces_dict, config_data, mode):
    """
    
    """
    interfaces = None

    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
    if interfaces and "ranges" in interfaces.keys():
        ranges = interfaces["ranges"]
        for range_dict in ranges:
            if mode == range_dict["mode"]:
                add_ranges_entry(ifaces_dict, range_dict)

def add_interface_entry(ifaces_dict, iface_dict, iface_name):
    """
    
    """
    # validate iface_dict
    # if iface_dict has no iface_name_prefix and no iface_id try convert iface_name.
    # if converting iface_name get iface_type and iface_id.
    # create an iface_dict entry with an iface_type, iface_id and lines if pressent.
    iface_dict = valid_interface_dict(iface_dict)
    print("ADD INTERFACE ENTRY")
    print(iface_name)
    print(iface_dict)
    if iface_name not in ifaces_dict.keys():
        ifaces_dict[iface_name] = iface_dict
    else:
        lines = iface_dict["lines"]
        for line in lines:
            ifaces_dict[iface_name]["lines"].append(line)
    print(iface_dict)

def add_ranges_entry(ifaces_dict, range_dict):
    """
    
    """
    # validate ranges dict.
    # if each iface_name not pressent in ifaces dict add entry.
    
    valid_ranges_dict(range_dict)

    iface_ids = range_dict["iface_ids"]
    iface_name_prefix = range_dict["iface_name_prefix"]

    for iface_id in iface_ids:
        iface_name = iface_name_prefix + iface_id
        if iface_name not in ifaces_dict.keys():
            ifaces_dict[iface_name] = {
                "iface_type":range_dict["iface_type"],
                "iface_id":iface_id,
                "mode":range_dict["mode"],
                "lines":range_dict["lines"]
            }
        elif iface_name in ifaces_dict.keys():
            lines = range_dict["lines"]
            for line in lines:
                ifaces_dict[iface_name]["lines"].append(line)
        
    return ifaces_dict

def validate_config(config_data):
    """
    
    """
    validate_conn_data(config_data)
    validate_globals(config_data)
    validate_interfaces(config_data)
    validate_ranges(config_data)

def validate_conn_data(config_data):
    """
    
    """
    
    if "connection_data" not in config_data.keys():
        raise KeyError("config data missing connection data entry")
    elif "connection_data" in config_data.keys():
        conn_data = config_data["connection_data"]

        required_keys = [
            "device",
            "device_type",
            "ip_address",
            "port",
            "username",
            "password",
            "secret"
        ]

        for required_key in required_keys:
            if required_key not in conn_data.keys():
                raise KeyError(
                    f"required key {required_key} missing from connection data"
                )

def validate_globals(config_data):
    """
    
    """

    globals = {}

    if "global" in config_data.keys():
        globals["global"] = config_data["global"]
            
    protocols = get_protocols(config_data)

    for protocol in protocols:
        proto_obj = config_data[protocol]
        if "global" in proto_obj.keys():
            globals[protocol] = proto_obj["global"]

    for protocol, lines in globals.items():
        if not isinstance(lines, list):
            raise TypeError("lines must be type list")
        for line in lines:
            if not isinstance(line, str):
                raise TypeError("line within lines list is not of type string")

def validate_interfaces(config_data):
    """
    
    """

    interfaces = {}

    if "interfaces" in config_data.keys():
        interfaces["interfaces"] = config_data["interfaces"]

    protocols = get_protocols(config_data)

    for protocol in protocols:
        proto_obj = config_data[protocol]
        if "interfaces" in proto_obj.keys():
            interfaces[protocol] = proto_obj["interfaces"]

    for protocol, ifaces in interfaces.items():
        for iface_name, iface_dict in ifaces.items():
            if iface_name != "ranges":
                try:
                    valid_interface_dict(iface_dict)
                except Exception as e:
                    raise Exception(f"{protocol} {iface_name} {e.__str__()}")

def validate_ranges(config_data):
    """
    
    """

    ranges = {}

    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
        if "ranges" in interfaces.keys():
            ranges["interfaces"] = interfaces["ranges"]

    protocols = get_protocols(config_data)

    for protocol in protocols:
        proto_obj = config_data[protocol]
        if "interfaces" in proto_obj.keys():
            interfaces = proto_obj["interfaces"]
            if "ranges" in interfaces.keys():
                ranges[protocol] = interfaces["ranges"]

    for protocol, ranges_list in ranges.items():
        for range_dict in ranges_list:
            try:
                valid_ranges_dict(range_dict)
            except Exception as e:
                raise Exception(f"{protocol} {e.__str__()}")

def valid_mode(dict_obj):
    """
    
    """

    valid_modes = [
        "before",
        "after",
        None
    ]

    if "mode" in dict_obj.keys():
        mode = dict_obj["mode"]
        if mode not in valid_modes:
            raise ValueError(f"mode is {mode}. must be 'before', 'after' or None")
    else:
        dict_obj["mode"] = None

    return dict_obj

def valid_lines(dict_obj):
    """
    
    """

    if "lines" in dict_obj.keys():
        lines = dict_obj["lines"]
        if not isinstance(lines, list):
            raise TypeError("lines must be type list")
        for line in lines:
            if not isinstance(line, str):
                raise TypeError("line within lines list is not of type string")
    else:
        dict_obj["lines"] = []

    return dict_obj

def valid_interface_dict(iface_dict):
    """
    
    """

    # iface_type, iface_id required keys.
    # if mode validate mode.
    # add mode and lines if not pressent.

    required_keys = [
        "iface_type",
        "iface_id"
    ]

    for k in required_keys:
        if k not in iface_dict.keys():
            raise KeyError(
                f"interface dict missing required entry {k}."
            )
        
    valid_mode(iface_dict)
        
    valid_lines(iface_dict)

    return iface_dict

def valid_ranges_dict(ranges_dict):
    """
    
    """
    
    # required keys iface_type, iface_ids.
    # if mode validate mode.
    # add mode and lines if not pressent.

    required_keys = [
        "iface_type",
        "iface_ids"
    ]

    for k in required_keys:
        if k not in ranges_dict.keys():
            raise KeyError(
                f"ranges dict does not contain required entry {k}"
            )
        
    valid_mode(ranges_dict)

    valid_lines(ranges_dict)
        
    return ranges_dict