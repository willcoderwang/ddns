# -*- coding:utf-8 -*-
import config
import utils
import logging
import namesilo


namesilo_token = 'namesilo_token'	# put your namesilo token here
domain = 'example.com'			# the domain to be updated

wan_ip = utils.get_wan_ip()

config_dict = config.read_config('ddns.conf')
requested_ip = config_dict.get('requested_ip')

if requested_ip == wan_ip:
    logging.info('wan_ip equals to requested_ip, this means:\n'
                 '1. everything is normal\n'
                 '2. resolution change request sent, you will have to wait for it to take effect')
    exit(0)
else:
    ns = namesilo.Namesilo(namesilo_token)
    ns.update_domain(domain, wan_ip)
    config_dict['requested_ip'] = wan_ip
    config.write_config('ddns.conf', config_dict)
