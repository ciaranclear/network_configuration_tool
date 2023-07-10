


def valid_config(config_data):

    valid_data = {}

    valid_conn_data(config_data, valid_data)
    valid_globals(config_data, valid_data)
    valid_interfaces(config_data, valid_data)
    valid_ranges(config_data, valid_data)

    return valid_data

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

def valid_conn_data(config_data, valid_data):
    
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
            
    valid_data["connection_data"] = conn_data

    return valid_data

def valid_globals(config_data, valid_data):
    
    globals = {}

    if "global" in config_data.keys():
        globals["global"] = config_data["global"]

    protocols = get_protocols(config_data)

    for protocol in protocols:
        if "global" in config_data[protocol].keys():
            globals[protocol] = config_data[protocol]["global"]

    for protocol, lines in globals.items():
        if not isinstance(lines, list):
            raise TypeError("lines must be type list")
        for line in lines:
            if not isinstance(line, str):
                raise TypeError("line within lines list is not of type string")
            
    valid_data["globals"] = globals

    return valid_data

def valid_interfaces(config_data, valid_data):
    
    ifaces_dict = {}

    valid_interfaces_dict = {}

    if "interfaces" in config_data.keys():
        ifaces_dict["interfaces"] = config_data["interfaces"]

    protocols = get_protocols(config_data)

    for protocol in protocols:
        if "interfaces" in config_data[protocol].keys():
            ifaces_dict[protocol] = config_data[protocol]["interfaces"]

    for protocol, interfaces in ifaces_dict.items():
        # must have iface_type.
        # must have iface_id.
        # if mode must be valid mode.
        # if no lines add lines list.

        valid_ifaces_dict = {}

        if not isinstance(interfaces, dict):
            raise TypeError(f"")
        
        for iface_name, interface in interfaces.items():
            if iface_name != "ranges":
                if not isinstance(interface, dict):
                    raise TypeError(f"")
                if "iface_type" not in interface.keys():
                    raise KeyError(f"")
                if "iface_id" not in interface.keys():
                    raise KeyError(f"")
                if "mode" in interface.keys():
                    if interface["mode"] not in ["before","after",None]:
                        raise ValueError(f"")
                if "lines" in interface.keys():
                    lines = interface["lines"]
                    if not isinstance(lines, list):
                        raise TypeError(f"")
                    for line in lines:
                        if not isinstance(line, str):
                            raise TypeError(f"")
                    
                valid_iface = {
                    "iface_type":interface["iface_type"],
                    "iface_id":interface["iface_id"]
                }

                if "mode" in interface.keys():
                    valid_iface["mode"] = interface["mode"]
                else:
                    valid_iface["mode"] = None

                if "lines" in interface.keys():
                    valid_iface["lines"] = interface["lines"]
                else:
                    valid_iface["lines"] = []

                valid_ifaces_dict[iface_name] = valid_iface

        valid_interfaces_dict[protocol] = valid_ifaces_dict

    valid_data["interfaces"] = valid_interfaces_dict

    return valid_data

def valid_ranges(config_data, valid_data):

    ranges_dict = {}

    valid_ranges_dict = {}

    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
        if "ranges" in interfaces.keys():
            ranges = interfaces["ranges"]
            ranges_dict["interfaces"] = ranges
    
    protocols = get_protocols(config_data)

    for protocol in protocols:
        if "interfaces" in config_data[protocol].keys():
            interfaces = config_data[protocol]["interfaces"]
            if "ranges" in interfaces.keys():
                ranges = interfaces["ranges"]
                ranges_dict[protocol] = ranges

    for protocol, ranges in ranges_dict.items():
        # must have iface_type.
        # must have iface_name_prefix.
        # must have iface_ids.
        # if mode check mode is valid.
        # if lines check valid lines.

        valid_ranges_list = []

        if not isinstance(ranges, list):
            raise TypeError(f"")
        
        for range_obj in ranges:
            if "iface_type" not in range_obj.keys():
                raise KeyError(f"")
            if "iface_name_prefix" not in range_obj.keys():
                raise KeyError(f"")
            if "mode" in range_obj.keys():
                if range_obj["mode"] not in ["before","after",None]:
                    raise ValueError(f"")
            if "lines" in range_obj.keys():
                lines = range_obj["lines"]
                if not isinstance(lines, list):
                    raise TypeError(f"")
                for line in lines:
                    if not isinstance(line, str):
                        raise TypeError(f"")
                    
            valid_range_obj = {
                "iface_type":range_obj["iface_type"],
                "iface_name_prefix":range_obj["iface_name_prefix"],
                "iface_ids":range_obj["iface_ids"]
            }

            if "mode" in range_obj.keys():
                valid_range_obj["mode"] = range_obj["mode"]
            else:
                valid_range_obj["mode"] = None

            if "lines" in range_obj.keys():
                valid_range_obj["lines"] = range_obj["lines"]
            else:
                valid_range_obj["lines"] = []

            valid_ranges_list.append(valid_range_obj)

        valid_ranges_dict[protocol] = valid_ranges_list

    valid_data["ranges"] = valid_ranges_dict

    return valid_data