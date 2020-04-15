"""
Module for geo-localization of IP addresses.
"""

import functools

from ipstack import GeoLookup

from utils import IP_STACK_KEY

# Create the GeoLookup object using custom API key (set in utils.py).
geo_lookup = GeoLookup(IP_STACK_KEY)
countries = ['China', 'Italy', 'Japan', 'Germany', 'France', 'Poland']

""" find the location of the passed ipv4/ipv6 address, caching values to reduce
the number of requests to "ipstack" service (limited to 10.000) """


@functools.lru_cache(maxsize=2048)
def lookup(host):
    location = geo_lookup.get_location(host)
    return location
