.. PubDNS documentation master file, created by
   sphinx-quickstart on Tue Dec 19 22:58:03 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PubDNS's documentation
======================
pubdns is a library for python to have more than 28K public dns servers from 190+ countries at your python script. it works based on the public-dns.info collected data and there is a wrapper based on the dnspython to resolve all type of dns records through these public dns server smoothly.

.. code-block:: python

   import pubdns
   pd = pubdns.pubdns()
   servers = pd.servers('US', 'los angeles')

pubdns module
---------------------

.. automodule:: pubdns.pubdns
    :members:
    :undoc-members:
    :show-inheritance:

dns module
------------------

.. automodule:: pubdns.dns
    :members:
    :undoc-members:
    :show-inheritance:

.. code-block:: python

   import pubdns
   pd = pubdns.pubdns()
   servers = pd.servers('US', 'new york')
   rs = pubdns.dns.resolver(servers, 'amazon.com', ['A'])
   for r in rs:
       print(r)

exceptions module
-------------------------

.. automodule:: pubdns.exceptions
    :members:
    :undoc-members:
    :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
