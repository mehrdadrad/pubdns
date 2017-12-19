"""
pubdns is a library for python to have public dns servers around
the world at your python script. it works based on the public-dns.info
collected data and there is a wrapper based on the dnspython to resolve
all type of dns records through these public dns server smoothly.

Usage is simple::

import pubdns
try:
    pd = pubdns.pubdns()
    servers = pd.servers('US', 'los angeles')
except pubdns.UpdateError as e:
    pass

Data sample:

{
 'city': 'Los Angeles', 'server': '12.127.16.67',
 'name': 'rmtu.mt.rs.els-gms.att.net.', 'reliability': '1.00'
}

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pubdns',
      version='0.1',
      description='Python Public DNS library',
      license='MIT',
      author='Mehrdad Arshad Rad',
      author_email='arshad.rad@gmail.com',
      url='https://github.com/mehrdadrad/pubdns',
      install_requires=['dnspython', 'requests'],
     )
