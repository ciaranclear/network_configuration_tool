"""
* save the device configuration string and configuration output.
"""
import os


def save_config(directory, cfg_input, cfg_output, device_name):

    directory = directory or "configs"
    if not os.path.isdir(directory):
        os.mkdir(directory)
    if os.path.isdir(directory):
        filepath = os.path.join(directory, f"{device_name}_inpt_str.txt")
        with open(filepath, "w") as f:
            f.write(cfg_input)
        filepath = os.path.join(directory, f"{device_name}_outp_str.txt")
        with open(filepath, "w") as f:
            f.write(cfg_output)

