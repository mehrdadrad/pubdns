from __future__ import print_function
import sys
import logging
import pubdns

logging.basicConfig(level=logging.DEBUG)

try:
    pd = pubdns.pubdns()
    servers = pd.servers('US', 'los angeles')
    rs = pubdns.dns.resolver(servers, 'amazon.com', ['A'])
    for r in rs:
        print(r)

except pubdns.UpdateError as e:
    logging.error(str(e))