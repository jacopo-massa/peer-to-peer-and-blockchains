"""
Module for loggin data, obtained by IPFS APIs.
"""

import functools
import re
from datetime import datetime

from multiaddr import Multiaddr
from multiaddr.exceptions import ProtocolLookupError
from timeloop import Timeloop

from geo_ip import lookup
from logger import setup_logger
from utils import *

# setup logger (reinitialized at every execution of the swarm check)
peer_log = setup_logger("main_logger", CSV_PATH)

# write the csv format (set in utils.py)
peer_log.info(re.sub("[{}]", "", CSV_FORMAT))

# timeloop service to run periodic tasks (used for a periodic analysis of the swarm)
tl = Timeloop()


# given a multiaddress, returns (if present) an IPv4 or IPv6 address, 'None' otherwise
@functools.lru_cache(maxsize=512)
def find_ip(multiaddress):
    try:
        ip4 = multiaddress['ip4']
    except ProtocolLookupError:
        ip4 = None

    try:
        ip6 = multiaddress['ip6']
    except ProtocolLookupError:
        ip6 = None

    return lookup(ip4) if ip4 else (lookup(ip6) if ip6 else None)


# given a peer, returns its info ad a python dict
def log_peer(peer):
    # needed because Multiaddr library not support ipfs protocol (suppressed by p2p)
    # for more info see this table:
    # https://github.com/multiformats/multiaddr/blob/master/protocols.csv
    multiaddr = Multiaddr(peer['Addr'].replace('/ipfs', '/p2p'))

    # get list of protocols in the multiaddress
    protocols = []
    for p in multiaddr.protocols():
        protocols.append(p.name)

    # find the location of the IP address
    location = find_ip(multiaddr)
    country = location['country_name'] if location else "Unknown"

    # retrieve the latency, converting it in milliseconds (as float)
    try:
        if peer['Latency'].endswith('ms'):  # latency in milliseconds
            latency = round(float(peer['Latency'].replace("ms", "")), 4)
        elif 'm' in peer['Latency']:  # latency in minutes
            latency_parts = peer['Latency'].split('m', 2)
            latency = (float(latency_parts[0]) * 60000) + float(latency_parts[1].replace("s", "")) * 1000
            latency = round(latency, 4)
        elif peer['Latency'].endswith('s'):  # latency in seconds
            latency = round(float(peer['Latency'].replace("s", "")) * 1000, 4)
        else:
            latency = ""
    except ValueError:
        latency = ""

    return {"peer": peer['Peer'],
            "protocols": "\"" + str(protocols) + "\"",
            "latency": latency,
            "country": country,
            "direction": peer['Direction']}


# job performed periodically to analyze the swarm
@tl.job(interval=TIME_DELTA)
def log_swarm():
    # get the list of peers in the swarm, with latency and connection's direction info
    peers = ipfs_request('/swarm/peers?latency=true&direction=true')['Peers']
    timestamp = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    for p in peers:
        peer_info = log_peer(p)
        peer_info['timestamp'] = timestamp
        peer_log.info(CSV_FORMAT.format(**peer_info))


if __name__ == '__main__':
    log_swarm()
    tl.start(block=True)
