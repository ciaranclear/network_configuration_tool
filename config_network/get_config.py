from pprint import pprint

def get_global_string(config_str, config_data):
    
    lines = []
    lines = get_global_lines(lines, config_data)
    lines = get_protocol_global_lines(lines, config_data)
    print("GLOBAL")
    print(lines)
    for line in lines:
        config_str += f"{line}\n"

    return config_str

def get_global_lines(lines, config_data):

    if "global" in config_data.keys():
        global_lines = config_data["global"]
        for line in global_lines:
            lines.append(line)

    return lines   

def get_protocol_global_lines(lines, config_data):

    for k, v in config_data.items():
        if k not in ["global","interfaces","connection_data"]:
            if "global" in v.keys():
                protocol_lines = v["global"]
                for line in protocol_lines:
                    lines.append(line)

    return lines

def get_interfaces_string(config_str, config_data):
    
    ifaces_dict = {}

    # protocol range lines before
    ifaces_dict = get_protocol_ranges_lines(ifaces_dict, config_data, "before")
    # interface lines
    ifaces_dict = get_ifaces_lines(ifaces_dict, config_data)
    # interface range lines
    ifaces_dict = get_ifaces_ranges_lines(ifaces_dict, config_data)
    # protocol lines
    ifaces_dict = get_protocol_ifaces_lines(ifaces_dict, config_data)
    # protocol range lines after
    ifaces_dict = get_protocol_ranges_lines(ifaces_dict, config_data, "after")
    pprint(ifaces_dict)
    for iface_name, iface in ifaces_dict.items():
        iface_type = iface["iface_type"]
        iface_id = iface["iface_id"]
        config_str += f"interface {iface_type} {iface_id}\n"
        lines = iface["lines"]
        for line in lines:
            config_str += f"{line}\n"
        config_str += "exit\n"

    return config_str

def get_ifaces_lines(ifaces_dict, config_data):
    
    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
        for iface_name, iface in interfaces.items():
            if iface_name != "ranges":
                # check if iface_name exists in iface_dict
                if iface_name in ifaces_dict.keys():
                    # if exists append lines to iface_dict lines
                    append_lines_to_interface(ifaces_dict, iface, iface_name)
                # if not exists create entry
                elif iface_name not in ifaces_dict.keys():
                    # iface must have iface_type, iface_id
                    for entry in ["iface_type","iface_id"]:
                        try:
                            iface[entry]
                        except KeyError:
                            raise Exception(
                                f"interface error!. interface {iface_name} missing "
                                f"required entry '{entry}' for interface id"
                            )
                    # add lines to new entry
                    if "lines" not in iface.keys():
                        iface["lines"] = []
                    ifaces_dict[iface_name] = iface

    return ifaces_dict

def get_ifaces_ranges_lines(ifaces_dict, config_data):
    
    if "interfaces" in config_data.keys():
        interfaces = config_data["interfaces"]
        if "ranges" in interfaces.keys():
            ranges = interfaces["ranges"]
            for range_obj in ranges:
                # range_obj must have entry for iface_type, iface_name_prefix, iface_ids
                valid_range_obj(range_obj)
                # for each iface_name
                iface_name_prefix = range_obj["iface_name_prefix"]
                for id in range_obj["iface_ids"]:
                    iface_name = f"{iface_name_prefix}{id}"
                    # if iface_name not in ifaces_dict add entry
                    add_interface_entry(ifaces_dict, range_obj, iface_name, id)
                    # if lines append lines
                    append_lines_to_interface(ifaces_dict, range_obj, iface_name)

    return ifaces_dict

def get_protocol_ifaces_lines(ifaces_dict, config_data):
    
    for k, v in config_data.items():
        if k not in ["connection_data","interfaces","global"]:
            # if interfaces in protocol append lines to ifaces_dict
            if "interfaces" in v.keys():
                interfaces = v["interfaces"]
                for iface_name, lines in interfaces.items():
                    if iface_name != "ranges":
                        if iface_name not in ifaces_dict.keys():
                            raise Exception(
                                f"{iface_name} not in ifaces_dict")
                        else:
                            for line in lines:
                                ifaces_dict[iface_name]["lines"].append(line)
    
    return ifaces_dict

def get_protocol_ranges_lines(ifaces_dict, config_data, mode):
    
    protocols = []

    for k in config_data.keys():
        if k not in ["connection_data","global","interfaces"]:
            protocols.append(k)

    ranges_dict = {}

    for protocol in protocols:
        if "interfaces" in config_data[protocol]:
            interfaces = config_data[protocol]["interfaces"]
            if "ranges" in interfaces.keys():
                ranges_dict[protocol] = interfaces["ranges"]

    for protocol, ranges in ranges_dict.items():
        for range_obj in ranges:
            range_mode = None
            if "mode" in range_obj.keys():
                range_mode = range_obj["mode"]
            if (range_mode == "before" and mode == "before") or \
               (mode == "after" and mode != range_mode):
                valid_range_obj(range_obj)
                iface_name_prefix = range_obj["iface_name_prefix"]
                for id in range_obj["iface_ids"]:
                    iface_name = f"{iface_name_prefix}{id}"
                    # if iface_name not in ifaces_dict add entry
                    add_interface_entry(ifaces_dict, range_obj, iface_name, id)
                    # if lines append lines
                    append_lines_to_interface(ifaces_dict, range_obj, iface_name)

    return ifaces_dict

def append_lines_to_interface(ifaces_dict, iface_obj, iface_name):
    if "lines" in iface_obj.keys():
        lines = iface_obj["lines"]
        for line in lines:
            ifaces_dict[iface_name]["lines"].append(line)

    return ifaces_dict

def add_interface_entry(ifaces_dict, range_obj, iface_name, id):
    if iface_name not in ifaces_dict.keys():
        ifaces_dict[iface_name] = {
            "iface_type":range_obj["iface_type"],
            "iface_id":id,
            "lines":[]
        }

def valid_range_obj(range_obj):
    for entry in ["iface_type","iface_name_prefix","iface_ids"]:
        if entry not in range_obj.keys():
            raise Exception(f"ranges error!. interfaces ranges object hsa no entry for '{entry}'")

def get_config_string(config_data):

    config_str = ""

    config_str = get_global_string(config_str, config_data)
    config_str = get_interfaces_string(config_str, config_data)

    return config_str