"""
Module contaning configuration variables.
"""

import os
from datetime import timedelta

import requests

""" PLOT """
DASH_PORT = 5002
DASH_ADDRESS = "http://127.0.0.1:{}".format(DASH_PORT)
DEFAULT_DIR = os.path.dirname(os.path.realpath(__file__))
TIME_DELTA = timedelta(hours=1, minutes=0, seconds=0)
IMG_PATH = os.path.join(DEFAULT_DIR, "img")

""" GEO IP """
IP_STACK_KEY = "ac00140885a5dca0d8277d8e946d227c"

""" LOG """
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M"
CSV_FORMAT = "{timestamp},{peer},{protocols},{latency},{direction},{country}"
CSV_PATH = os.path.join(DEFAULT_DIR, "log", "log.csv")

""" IPFS UTILS """
IPFS_API_ADDRESS = "http://127.0.0.1:5001/api/v0"


# Function to call IPFS HTTP APIs, using the python module 'requests'
# Needs a running ipfs daemon to works correctly
def ipfs_request(method, **kwargs):
    try:
        response = requests.get(IPFS_API_ADDRESS + method, params=kwargs)
        return response.json()
    except requests.exceptions.ConnectionError:
        raise SystemExit("Start the IPFS daemon before starting this script.\n"
                         "To start the IPFS daemon, execute: \"ipfs daemon\" command on shell.")
