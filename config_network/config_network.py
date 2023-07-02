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
from config_device import config_device
from save_config import save_config
import argparse
import json
import os


def config_network(argv=None):

    # get inventory filepath and optional output directory path
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory_filename")
    parser.add_argument("-o", "--output_directory")
    args = parser.parse_args()

    # get configs using inventory file
    with open(args.inventory_filename, "r") as f:
        inventory_data = json.loads(f.read())

        for device_name, filename in inventory_data.items():
            dirpath = os.path.dirname(args.inventory_filename)
            print(filename)
            filepath = os.path.join(dirpath, filename)

            # get formatted configuration string
            with open(filepath, "r") as f:
                config_data = json.loads(f.read())
                config_string = get_config_string(config_data)
                print(config_string)
                # configure devices
                print(f"CONFIGURING {device_name}")
                conn_data = config_data["connection_data"]
                output = config_device(conn_data, config_string)

                # store configuration output
                save_config(args.output_directory ,config_string, output, device_name)

if __name__ == "__main__":
    config_network()
