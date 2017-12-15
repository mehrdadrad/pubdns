"""
public dns python module
"""
import logging
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
        except Exception as e:
            logging.debug(e)
            self.update()

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
                       name=fields[m['name']], reliability=fields[m['reliability']])
            self.data[fields[m['country_id']]].append(rec)

    def _load_data(self):
        filename = os.path.join(self.home, '.publicdns')
        with open(filename, 'r') as f:
            PubDNS.data = json.load(f)

    def _save_data(self):
        filename = os.path.join(self.home, '.publicdns')
        with open(filename, 'w') as f:
            f.write(json.dumps(PubDNS.data))

    def xservers(self, country_id, city=''):
        """ Return servers based on the country / city """

        if country_id not in PubDNS.data:
            return {}

        city = city.lower()
        for rec in PubDNS.data[country_id]:
            if city == '' or rec['city'].lower() == city:
                yield rec

    def servers(self, country_id, city=''):
        """ Return servers based on the country / city """

        if country_id not in PubDNS.data:
            return {}

        city = city.lower()
        if city == '':
            return PubDNS.data[country_id]
        else:
            recs = []
            for rec in PubDNS.data[country_id]:
                if city == '' or rec['city'].lower() == city:
                    recs.append(rec)
            return recs       

    def update(self):
        """ Fetch and save pub dns info """

        try:
            csv_data = self._get_data()
            self._normalize(csv_data)
            self._save_data()
        except Exception as e:
            logging.debug(e)
            raise 'Can not fetch / update public dns'

def pubdns():
    """ Return a :class:`PubDNS` """

    return PubDNS()
