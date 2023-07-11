
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
        try:
            config_data = valid_config(config_data)
            valid_config_data[device_name] = config_data
        except Exception as e:
            raise Exception(f"{device_name} {e.__str__()}")

    return valid_config_data

def get_config_strings(config_data):

    config_strings = {}

    for device_name, config in config_data.items():
        config_string = get_config_string(config)
        config_strings[device_name] = config_string

    return config_strings

def get_initial_settings(config_data):
    
    initial_configs = {}

    commands = ["run", "start"]

    for device_name, config in config_data.items():
        conn_data = config["connection_data"]
        init_configs = get_initial_configs(conn_data, commands)
        initial_configs[device_name] = init_configs

    return initial_configs

def configure_device(device_name, conn_data, config_string, output_dict):
    print(f"CONFIGURING {device_name}")
    output = config_device(conn_data, config_string)
    print(f"FINISHED CONFIGURING {device_name}")
    output_dict[device_name] = {
        "input_str":config_string,
        "output_str":output
    }

def display_errors(output_dict):
    
    for device_name, output in output_dict.items():
        lines = output["output_str"].split("\n")

        for i, line in enumerate(lines):
            if len(line) != 0 and line[0] == "%":
                print(f"Error in output config in {device_name}")
                print(lines[i-1])
                print(line)

def store_results(initial_settings, output_dict, args):
    # make output directory if it does not exist.
    # make sub directory for each device name.
    # within each device directory create a pre and post directory.
    # inside pre directory store the initial settings.
    # in post directory store the device input configuration string and
    # the output configuration string.
    dirpath = args.output_directory or os.path.dirname(args.inventory_filename)
    dirpath = os.path.join(dirpath, "configs")
    os.mkdir(dirpath)

    device_list = initial_settings.keys()

    for device_name in device_list:
        device_directory = os.path.join(dirpath, device_name)
        os.mkdir(device_directory)
        pre_directory = os.path.join(device_directory, 'pre_config')
        os.mkdir(pre_directory)
        post_directory = os.path.join(device_directory, "post_config")
        os.mkdir(post_directory)
        initial_setting_dict = initial_settings[device_name]
        for command, setting_str in initial_setting_dict.items():
            filepath = os.path.join(pre_directory, f"{command}.txt")
            with open(filepath, "w") as f:
                f.write(setting_str)

        for k, v in output_dict[device_name].items():
            filepath = os.path.join(post_directory, f"{k}.txt")
            with open(filepath, "w") as f:
                f.write(v)
    
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

    store_results(initial_settings, output_dict, args)

if __name__ == "__main__":
    config_network()
