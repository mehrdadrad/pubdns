"""
public dns python module
"""

import os
import json
import collections
import requests

class PubDNS(object):
    """ PubDNS class """

    host = 'https://public-dns.info/nameservers.csv'
    data = collections.defaultdict(list)

    def __init__(self):
        self.home = os.path.expanduser("~")
        self.disable_cache = False

        try:
            self._load_data()
        except:
            csv_data = self._get_data()
            self._normalize(csv_data)
            self._save_data()

    def _get_data(self):
        try:
            resp = requests.get(PubDNS.host)
            return resp.text
        except:
            raise 'can not fetch data from origin'

    def _normalize(self, csv_data):
        rows = csv_data.split('\n')
        m = {x:y for y, x in enumerate(rows[0].split(','))}

        for row in rows[1:]:
            fields = row.split(',')
            if len(fields) < 4 or fields[m['city']] == '':
                continue
            rec = dict(city=fields[m['city']], server=fields[m['ip']],
                       reliability=fields[m['reliability']])
            self.data[fields[m['country_id']]].append(rec)

    def _load_data(self):
        try:
            filename = os.path.join(self.home, '.publicdns.csv')
            with open(filename, 'r') as f:
                PubDNS.data = json.load(f)

        except:
            raise 'can not load data from local drive'

    def _save_data(self):
        try:
            filename = os.path.join(self.home, '.publicdns.csv')
            with open(filename, 'w') as f:
                f.write(json.dumps(PubDNS.data))
        except:
            raise 'can not save data to local drive'

    def get_servers(self, country_id, city=''):
        """ Return servers based on the country / city """

        if country_id not in PubDNS.data:
            return {}

        if city != '':
            for rec in PubDNS.data[country_id]:
                if rec['city'] == city:
                    yield rec
        return (x for x in PubDNS.data[country_id])

def pubdns():
    """ Return a :class:`PubDNS` """

    return PubDNS()
