"""
* save the device configuration string and configuration output.
"""
import os


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
