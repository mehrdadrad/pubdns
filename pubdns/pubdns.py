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
    """PubDNS class

    :param cache_dir: (optional) The cache storage directory
    :param host: (optional) If you need to put public-dns.info csv
        data at another host.
    :param proxies: (optional) If you need to use a proxy, you can
        configure individual.
        requests with the proxies argument to any request method:
        proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
        }
        You can also configure proxies by setting the environment
        variables HTTP_PROXY and HTTPS_PROXY
    :param timeout: (optional) Connection response timeout seconds
    :param cache_disabled: (optional) Disable caching
    """

    data = collections.defaultdict(list)

    def __init__(self, cache_dir=None, host=None, proxies=None,
                 timeout=1, cache_disabled=False):

        public_dns = 'http://public-dns.info/nameservers.csv'
        home_dir = os.path.expanduser("~")

        self.cache_dir = home_dir if cache_dir is None else cache_dir
        self.host = public_dns if host is None else host
        self.proxies = {} if proxies is None else proxies
        self.cache_disabled = cache_disabled
        self.timeout = timeout

        try:
            self._load_data()
        except Exception as e:
            logging.debug(e)
            self.update()

    def _get_data(self):
        resp = requests.get(self.host, timeout=self.timeout,
                            proxies=self.proxies)
        if resp.status_code == 200:
            return resp.text
        else:
            err = "HTTP error code: {}".format(resp.status_code)
            raise Exception(err)

    def _normalize(self, csv_data):
        rows = csv_data.split('\n')
        m = {x: y for y, x in enumerate(rows[0].split(','))}
        if 'ip' not in m:
            m['ip'] = m['ip_address']
            del m['ip_address']
        if 'country_id' not in m:
            m['country_id'] = m['country_code']
            del m['country_code']

        for row in rows[1:]:
            fields = row.split(',')
            if len(fields) < len(m) - 1 or fields[m['city']] == '':
                continue
            rec = dict(city=fields[m['city']], server=fields[m['ip']],
                       name=fields[m['name']],
                       reliability=fields[m['reliability']])
            self.data[fields[m['country_id']]].append(rec)

    def _load_data(self):
        filename = os.path.join(self.cache_dir, '.publicdns')
        with open(filename, 'r') as f:
            PubDNS.data = json.load(f)

    def _save_data(self):
        if self.cache_disabled:
            logging.debug('cache is disabled')
            return

        filename = os.path.join(self.cache_dir, '.publicdns')
        with open(filename, 'w') as f:
            f.write(json.dumps(PubDNS.data))

    def rand_server(self, country_id=""):
        """Return a random public dns server

        :param country_id: two-letter ISO 3166-1 of the country, optional

        :rtype: dict
        """

        if country_id == "":
            country_id = random.choice(list(self.data.keys()))
        try:
            rand = random.choice(self.data[country_id])
            rand = rand.copy()
            rand.update({'country_id': country_id})
            return rand
        except IndexError:
            return {}

    def set_server(self, server):
        """Add a custom dns server in memory

        :param server: a server dict including below keys:
            - country_id: two letter ISO 3166-1
            - city: city name
            - name: dns name
            - server: ip address
            - reliability: reliability number
        """

        country_id = server['country_id']
        del server['country_id']
        if country_id in self.data:
            self.data[country_id].append(server)
        else:
            self.data[country_id] = []
            self.data[country_id].append(server)

    def xservers(self, country_id, city=''):
        """Return a generator of servers based on the country / city

        :param country_id: two-letter ISO 3166-1 alpha-2 code of the country
        :param city: the city that the server is hosted on, optional

        :rtype: Generator[dict]
        """

        country_id = country_id.upper()
        rows = PubDNS.data.get(country_id, [])

        city = city.lower()
        for row in rows:
            if city == '' or row['city'].lower() == city:
                yield row

    def servers(self, country_id, city=''):
        """Return servers based on the country / city

        :param country_id: two-letter ISO 3166-1 alpha-2 code of the country
        :param city: the city that the server is hosted on

        :rtype: list
        """

        country_id = country_id.upper()
        rows = PubDNS.data.get(country_id, [])

        city = city.lower()
        if city == '':
            return rows

        res = []
        for row in rows:
            if city == '' or row['city'].lower() == city:
                res.append(row)
        return res

    def update(self, ttl=1440):
        """Fetch and store public-dns.info dns servers information

        :param ttl: update checks cache last modified time and updates
            if it expired based on the specified TTL. defaults to ``1440``
            the unit is minute.
        """

        if ttl != 0 and time.time() / 60 - self._last_update() < ttl:
            logging.debug('Public dns cache is not expired')
            return

        try:
            csv_data = self._get_data()
            self._normalize(csv_data)
            self._save_data()
        except Exception as e:
            logging.debug(e)
            raise UpdateError('Can not fetch or update public dns')

    def _last_update(self):
        """Return last update timestamp """

        filename = os.path.join(self.cache_dir, '.publicdns')
        if not os.path.isfile(filename):
            return 0
        return os.path.getmtime(filename) / 60


def pubdns(**kwargs):
    """Return a :class:`PubDNS` """

    return PubDNS(**kwargs)
