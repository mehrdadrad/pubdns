"""
PubDNS is a python library to interact with public DNS servers around the world

Usage:
    >>> import pubdns
    >>> pd = pubdns.pubdns()
    >>> servers = pd.servers('US')
    >>> print(len(servers))
    2714
    >>> print(servers.pop())
    {
        'city': 'San Francisco',
        'server': '162.243.136.199',
        'name': '',
        'reliability': '1.00'
    }

:license: MIT
"""

from .pubdns import pubdns, PubDNS
from .dns import resolver
from .exceptions import UpdateError

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__

__all__ = ['pubdns', 'dns', 'PubDNS']
