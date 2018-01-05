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
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'pubdns', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    descr = f.read()

setup(name='pubdns',
      version=about['__version__'],
      description=about['__description__'],
      long_description=descr,
      license=about['__license__'],
      author=about['__author__'],
      author_email=about['__author_email__'],
      url=about['__url__'],
      packages=['pubdns'],
      tests_require=['mock'],
      test_suite="tests",
      classifiers=(
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ),
      install_requires=['dnspython', 'requests'],
     )
