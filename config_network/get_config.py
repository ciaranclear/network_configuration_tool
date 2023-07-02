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
        # get before ranges in interfaces
        if "ranges" in interfaces.keys():
            ranges = interfaces["ranges"]
            for range_obj in ranges:
                if "mode" in range_obj.keys() and range_obj["mode"] == "before":
                    iface_type = range_obj["iface_type"]
                    iface_name_prefix = range_obj["iface_name_prefix"]
                    iface_ids = range_obj["iface_ids"]
                    lines = range_obj["lines"]
                    for id in iface_ids:
                        iface_name = f"{iface_name_prefix}{id}"
                        if iface_name not in interfaces_dict.keys():
                            interfaces_dict[iface_name] = {
                                "iface_type":iface_type,
                                "iface_id":id,
                                "lines":lines
                            }
                        elif iface_name in interfaces_dict.keys():
                            for line in lines:
                                interfaces_dict[iface_name]["lines"].append(line)

        for iface_name, interface in interfaces.items():
            if iface_name != "ranges":
                if iface_name not in interfaces_dict.keys():
                    interfaces_dict[iface_name] = interface
                elif iface_name in interfaces_dict.keys():
                    lines = interface["lines"]
                    for line in lines:
                        interfaces_dict[iface_name]["lines"].append(line)

        # get after ranges in interfaces
        if "ranges" in interfaces.keys():
            ranges = interfaces["ranges"]
            for range_obj in ranges:
                if ("mode" in range_obj.keys() and range_obj["mode"] == "before") or \
                   ("mode" not in range_obj.keys()):
                    iface_type = range_obj["iface_type"]
                    iface_name_prefix = range_obj["iface_name_prefix"]
                    iface_ids = range_obj["iface_ids"]
                    lines = range_obj["lines"]
                    for id in iface_ids:
                        iface_name = f"{iface_name_prefix}{id}"
                        if iface_name not in interfaces_dict.keys():
                            interfaces_dict[iface_name] = {
                                "iface_type":iface_type,
                                "iface_id":id,
                                "lines":lines
                            }
                        elif iface_name in interfaces_dict.keys():
                            for line in lines:
                                interfaces_dict[iface_name]["lines"].append(line)

    # get interfaces lines for each protocol
    for k, v in config_data.items():
        if k not in ["global","interfaces","connection_data"]:
            if "interfaces" in v.keys():
                interfaces = v["interfaces"]
                # get before ranges in each protocol
                if "ranges" in interfaces.keys():
                    ranges = interfaces["ranges"]
                    for range_obj in ranges:
                        if "mode" in range_obj.keys() and range_obj["mode"] == "before":
                            iface_type = range_obj["iface_type"]
                            iface_name_prefix = range_obj["iface_name_prefix"]
                            iface_ids = range_obj["iface_ids"]
                            lines = range_obj["lines"]
                            for id in iface_ids:
                                iface_name = f"{iface_name_prefix}{id}"
                                for line in lines:
                                    interfaces_dict[iface_name]["lines"].append(line)        

                for iface_name, lines in interfaces.items():
                    if iface_name != "ranges":
                        for line in lines:
                            interfaces_dict[iface_name]["lines"].append(line)

                # get after ranges in each protocol
                if "ranges" in interfaces.keys():
                    ranges = interfaces["ranges"]
                    for range_obj in ranges:
                        if ("mode" in range_obj.keys() and range_obj["mode"] == "before") or \
                           ("mode" not in range_obj.keys()):
                            iface_type = range_obj["iface_type"]
                            iface_name_prefix = range_obj["iface_name_prefix"]
                            iface_ids = range_obj["iface_ids"]
                            lines = range_obj["lines"]
                            for id in iface_ids:
                                iface_name = f"{iface_name_prefix}{id}"
                                for line in lines:
                                    interfaces_dict[iface_name]["lines"].append(line) 

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
