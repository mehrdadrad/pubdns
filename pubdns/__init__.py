from .pubdns import pubdns, PubDNS
from .dns import resolver
from .exceptions import UpdateError

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__

__all__ = ['pubdns', 'dns', 'PubDNS']
