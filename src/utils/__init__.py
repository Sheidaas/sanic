import os
from configparser import ConfigParser


def read_config_file(root_path: str):
    config_parser = ConfigParser()
    config_parser.read(os.path.join(root_path, 'resources', 'config.ini'))
    return config_parser
