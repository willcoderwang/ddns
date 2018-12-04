# -*- coding:utf-8 -*-
import requests
import logging


def get_wan_ip():
    r = requests.get('https://icanhazip.com')

    if r.status_code != 200:
        logging.error('can not connect to icanhazip.com to get wan ip')
        exit(1)

    return r.text[:-1]
