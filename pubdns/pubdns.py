"""
public dns python module
"""
import logging
import os
import json
import collections
import time
import random
import requests

from .exceptions import UpdateError

class PubDNS(object):
    """ PubDNS class """

    data = collections.defaultdict(list)

    def __init__(self):
        self.home = os.path.expanduser("~")
        self.disable_cache = False
        self.host = 'https://public-dns.info/nameservers.csv'

        try:
            self._load_data()
        except Exception as e:
            logging.debug(e)
            self.update()

    def _get_data(self):
        resp = requests.get(self.host)
        if resp.status_code == 200:
            return resp.text
        else:
            err = "HTTP error code: {}".format(resp.status_code)
            raise Exception(err)

    def _normalize(self, csv_data):
        rows = csv_data.split('\n')
        m = {x:y for y, x in enumerate(rows[0].split(','))}

        for row in rows[1:]:
            fields = row.split(',')
            if len(fields) < len(m) -1 or fields[m['city']] == '':
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

    def rand_server(self, country_id=""):
        """ Return random server """
        if country_id == "":
            country_id = random.choice(list(self.data.keys()))
        try:
            rand = random.choice(self.data[country_id])
            rand = rand.copy()
            rand.update({'country_id': country_id})
            return rand
        except IndexError:
            return {}

    def set_server(self, value):
        """ Add a server manually to data """
        country_id = value['country_id']
        del value['country_id']
        if country_id in self.data:
            self.data[country_id].append(value)
        else:
            self.data[country_id] = []
            self.data[country_id].append(value)

    def xservers(self, country_id, city=''):
        """ Return servers based on the country / city """

        records = PubDNS.data.get(country_id, [])

        city = city.lower()
        for rec in records:
            if city == '' or rec['city'].lower() == city:
                yield rec

    def servers(self, country_id, city=''):
        """ Return servers based on the country / city """

        if country_id not in PubDNS.data:
            return {}

        city = city.lower()
        if city == '':
            return PubDNS.data[country_id]

        recs = []
        for rec in PubDNS.data[country_id]:
            if city == '' or rec['city'].lower() == city:
                recs.append(rec)
        return recs

    def update(self, ttl=1440):
        """ Fetch and save pub dns info """

        if ttl != 0 and time.time()/60 - self._last_update() < ttl:
            logging.debug('public dns cache is not expired')
            return

        try:
            csv_data = self._get_data()
            self._normalize(csv_data)
            self._save_data()
        except Exception as e:
            logging.debug(e)
            raise UpdateError('Can not fetch or update public dns')

    def _last_update(self):
        """ Return last update timestamp """

        filename = os.path.join(self.home, '.publicdns')
        if not os.path.isfile(filename):
            return 0
        return os.path.getmtime(filename)/60


def pubdns():
    """ Return a :class:`PubDNS` """

    return PubDNS()
