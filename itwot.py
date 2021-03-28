"""A utility module that provides handy setup for the redirection on the itWoT machines"""

import re
import platform
import argparse

__PORTS = {
    "w07": 3000,
    "w08": 3500,
    "w09": 4000,
    "w10": 4500,
    "w11": 5000,
    "w12": 5500,
    "opg3": 6000,
    "opg4a": 6500,
    "opg4b": 7000,
}


def __parse_cmd_arguments() -> argparse.Namespace:
    """Parses command line arguments for the configuration

    Returns:
        argparse.Namespace: the given arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--redirection",
        choices=__PORTS.keys(),
        help="The name of the redirection",
    )
    return parser.parse_args()


def config() -> dict:
    """Creates a dict with the correct configurartion parameters
    for running locally and on the itWoT machines

    Returns:
        dict: The configuration parameters
    """
    args = __parse_cmd_arguments()
    _config = {"prefix": "", "port": 5000, "debug": True}
    redirection = args.redirection
    if redirection in __PORTS:
        _config["port"] = __PORTS[redirection]
    match = re.match(r"cs-itwot-(\d+)\.uni\.au\.dk", platform.node())
    if match:
        machine_no = match.group(1)
        if not redirection:
            redirection = "w11"
        _config["prefix"] = f"https://itwot.cs.au.dk/VM{machine_no}/{redirection}"
        _config["debug"] = False
    return _config


if __name__ == "__main__":
    print(config())