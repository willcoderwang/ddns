# -*- coding:utf-8 -*-
import domain_provider
from urllib.parse import urlencode
import requests
import logging
import xml.etree.ElementTree as ET


class Namesilo(domain_provider.DomainProvider):

    def __init__(self, key):
        super().__init__()
        self.key = key

    def update_domain(self, domain, value):
        records = self.get_records(domain)

        a_records = [record for record in records if record['record_type'] == 'A']

        url = 'https://www.namesilo.com/api/dnsUpdateRecord?'

        for r in a_records:
            if r['record_host'] == domain:
                rrhost = ''
            else:
                rrhost = r['record_host'][:len(r['record_host']) - len(domain) - 1]

            params = {
                'version': 1,
                'type': 'xml',
                'key': self.key,
                'domain': domain,
                'rrid': r['record_id'],
                'rrhost': rrhost,
                'rrvalue': value,
            }

            req = url + urlencode(params)

            resp = requests.get(req)

            if resp.status_code != 200:
                logging.error('error updating namesilo dnsUpdateRecord')
                exit(1)

    def get_records(self, domain):
        url = 'https://www.namesilo.com/api/dnsListRecords?'
        params = {
            'version': 1,
            'type': 'xml',
            'key': self.key,
            'domain': domain,
        }

        url += urlencode(params)

        resp = requests.get(url)

        if resp.status_code != 200:
            logging.error('error getting namesilo dnsListRecords')
            exit(1)

        root = ET.fromstring(resp.text)

        res = []
        for resource_record in root.iter('resource_record'):
            record_type = resource_record.find('type').text
            record_id = resource_record.find('record_id').text
            host = resource_record.find('host').text
            value = resource_record.find('value').text
            record = {
                'record_id': record_id,
                'record_type': record_type,
                'record_host': host,
                'record_value': value,
            }
            res.append(record)

        return res
