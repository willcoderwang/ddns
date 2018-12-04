# -*- coding:utf-8 -*-
import json
import logging
import os


def read_config(filename):
    res = dict()

    if not os.path.exists(filename):
        logging.warning('config file not exists, using default config instead')
        return res

    with open(filename, 'r') as f:
        config_content = f.read()
        try:
            res = json.loads(config_content)
        except Exception:
            logging.warning('error parsing config file, using default config instead')

    return res


def write_config(filename, config_dict):
    if not isinstance(config_dict, dict):
        logging.error('error writing to config file: config is not dict')
        exit(1)

    config_str = json.dumps(config_dict)

    with open(filename, 'w') as f:
        f.write(config_str)
