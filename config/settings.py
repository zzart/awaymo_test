""" Basic configurations and defaults"""

import os
from configparser import ConfigParser
from typing import Any

CURRENT_PATH = os.path.abspath(os.path.dirname(__name__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = ConfigParser()
# get variables from config file
CONFIG.read(os.path.join(BASE_DIR, 'config/config.ini'))


def get_config(key: str, as_bool=False, as_int=False, as_list=False)->Any:
    """
    Get configuration variables from `default` section.
    NOTE: ideally we would like to have 'dev', 'prod' etc. sections as well,
    but for now we just hard code the 'default`
    :param key: str key
    :param as_bool: bool, cast into bool
    :param as_int: bool, cast into int
    :param as_list: list, cast into list
    :return: config value or None
    """
    try:
        if as_bool:
            out = CONFIG.getboolean('DEFAULT', key)
        elif as_int:
            out = CONFIG.getint('DEFAULT', key)
        elif as_list:
            out = CONFIG.get('DEFAULT', key).split(',')
        else:
            out = CONFIG.get('DEFAULT', key)
    except KeyError:
        return None
    else:
        return out
