from __future__ import absolute_import
import dns.resolver
import dns.message
import logging


def resolver(servers, name, addr_types=['A'], timeout=1):
    for server in servers:
        for addr_type in addr_types:
            try:
                res = _resolver(server, name, addr_type, timeout)
                yield dict(server=server, resolve=res)
            except Exception as e:
                logging.debug(e)
                yield dict(server=server, resolve=[], error=str(e))

def _resolver(server, name, addr_type, timeout=1):
    res = []
    qname = dns.name.from_text(name)
    q = dns.message.make_query(qname, addr_type)
    r = dns.query.udp(q, server['server'], timeout=timeout)
    for rrset in r.answer:
        for rr in rrset.to_rdataset():
            res.append(dict(name=str(rr), type=rr.rdtype))

    return res
