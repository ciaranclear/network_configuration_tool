
# 1. get inventory file
# 2. get device configuration files.
# 3. validate device configuration files.
# 4. get device configuration strings.
# 5. get initial settings for each device.
# 6. push configuration string to each device.
# 7. display errors in each output string.
# 8. store output for each device.

from valid_config import valid_config
from get_config import get_config_string
from get_initial_configs import get_initial_configs
from config_device import config_device
import threading
import argparse
import json
import os


def get_inventory(inventory_filename):
  with open(inventory_filename, "r") as f:
        inventory = json.loads(f.read())
        return inventory

def get_config_data(filepath):
    with open(filepath, "r") as f:
        config_data = json.loads(f.read())
        return config_data

def get_config_data_dict(inventory, args):

    config_dict = {}

    for device_name, filename in inventory.items():
        dirpath = os.path.dirname(args.inventory_filename)
        filepath = os.path.join(dirpath, filename)

        config_data = get_config_data(filepath)
        config_dict[device_name] = config_data

    return config_dict

def get_valid_config_data(config_data_dict):

    valid_config_data = {}
    
    for device_name, config_data in config_data_dict.items():
        config_data = valid_config(config_data)
        valid_config_data[device_name] = config_data

    return valid_config_data

def get_config_strings(config_data):

    config_strings = {}

    for device_name, config in config_data.items():
        config_string = get_config_string(config)
        config_strings[device_name] = config_string

    return config_strings

def get_initial_settings(config_data):
    
    initial_configs = {}

    commands = ["show run", "show start"]

    for device_name, config in config_data.items():
        conn_data = config["connection_data"]
        init_configs = get_initial_configs(conn_data, commands)
        initial_configs[device_name] = init_configs

    return initial_configs

def configure_device(device_name, conn_data, config_string, output_dict):
    print(f"CONFIGURING {device_name}")
    output = config_device(conn_data, config_string)
    print(f"FINISHED CONFIGURING {device_name}")
    output_dict[device_name] = output

def display_errors(output_dict):
    
    for device_name, output in output_dict.items():
        lines = output.split("\n")

        for i, line in enumerate(lines):
            if len(line) != 0 and line[0] == "%":
                print(f"Error in output config in {device_name}")
                print(lines[i-1])
                print(line)

"""
def store_results(initial_settings, output_dict, args):
    # if no output directory default to config directory
    dirpath = os.path.dirname(args.inventory_filename)
    output_dir = args.output_directory or os.path.join(dirpath, "configs")
    # inside output directory create a sub directory called configs
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    # inside configs create a subdirectory pre_configs and post_configs
    pre_dirpath = os.path.join(output_dir, "pre_configs")
    if not os.path.isdir(pre_dirpath):
        os.mkdir(pre_dirpath)

    post_dirpath = os.path.join(output_dir, "post_configs")
    if not os.path.isdir(post_dirpath):
        os.mkdir(post_dirpath)

    # in pre_configs and post_configs create sub directory for each device
    device_pre_dirpath = os.path.join(pre_dirpath, device_name)
    if not os.path.isdir(device_pre_dirpath):
        os.mkdir(device_pre_dirpath)

    device_post_dirpath = os.path.join(post_dirpath, device_name)
    if not os.path.isdir(device_post_dirpath):
        os.mkdir(device_post_dirpath)

    # save the files to each devices directory
    save_configs(device_pre_dirpath, initial_configs)
    output_configs = {
        "input_string":config_string,
        "output_string":output
    }
    save_configs(device_post_dirpath, output_configs)
"""

def save_configs(dirpath, configs):

    # resolve the directory in this module.
    # if no directory default directory will be in the configuration directory
    # in save directory create a sub directory with the device name.
    # save the initial configs
    # save the input configuration string.
    # save the output configuration string.

    for cfg_name, cfg_string in configs.items():
        fpath = os.path.join(dirpath, cfg_name)
        with open(f"{fpath}.txt", "w") as f:
            f.write(cfg_string)
    
def config_network(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("inventory_filename")
    parser.add_argument("-o", "--output_directory")
    args = parser.parse_args()

    inventory_filename = args.inventory_filename

    inventory = get_inventory(inventory_filename)

    config_data = get_config_data_dict(inventory, args)

    valid_configs = get_valid_config_data(config_data)

    config_strings = get_config_strings(valid_configs)

    initial_settings = get_initial_settings(valid_configs)

    output_dict = {}

    threads = []

    for device_name, config_string in config_strings.items():
        conn_data = valid_configs[device_name]["connection_data"]
        args_list = [device_name, conn_data, config_string, output_dict]
        t = threading.Thread(target=configure_device, args=args_list)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    display_errors(output_dict)

    #store_results(initial_settings, output_dict, args)

if __name__ == "__main__":
    config_network()
