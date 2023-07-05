"""
* get inventory filepath.
* get optional output directory path.
* get configs using inventory file.
* get formatted configuration string.
* call device configuration function.
* store configuration results.

###### NOTES ######

* the inventory fileshould be in the same directory as the configurations.
"""
from get_config import get_config_string
from get_initial_configs import get_initial_configs
from config_device import config_device
from save_configs import save_configs
import argparse
import json
import os


def get_inventory(args):
  with open(args.inventory_filename, "r") as f:
        inventory = json.loads(f.read())
        return inventory

def get_config_data(filepath):
    with open(filepath, "r") as f:
        config_data = json.loads(f.read())
        return config_data

def config_network(argv=None):

    # get inventory filepath and optional output directory path
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory_filename")
    parser.add_argument("-o", "--output_directory")
    args = parser.parse_args()

    # get configs using inventory file
    inventory = get_inventory(args)

    for device_name, filename in inventory.items():
        dirpath = os.path.dirname(args.inventory_filename)
        filepath = os.path.join(dirpath, filename)

        # get formatted configuration string
        config_data = get_config_data(filepath)
        config_string = get_config_string(config_data)
        # configure devices
        print(f"CONFIGURING {device_name}")
        conn_data = config_data["connection_data"]
        # get initial configs
        initial_configs = get_initial_configs(conn_data, ["startup-config","running-config"])
        # configure device
        output = config_device(conn_data, config_string)
        # save configs

        # if no output directory default to config directory
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

if __name__ == "__main__":
    config_network()
