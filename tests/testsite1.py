#!/usr/bin/env python3

import os
import time

import glasto as gl

# test on reference HTML obtained from todays resale
URL = "file:///{}/ref/Buy%20tickets%20for%20Glastonbury%202020%20-%20Glastonbury.html".format(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
URL = "http://localhost:3000/Buy%20tickets%20for%20Glastonbury%202023%20-%20Glastonbury.html"
PHRASES_TO_CHECK = gl.Twenty23.REGISTRATION_PHRASE

REG_DETAILS = [
    {"number": "154414413", "postcode": "N7 0DU"},
    {"number": "390811765", "postcode": "N7 0DU"},
    {"number": "3069133115", "postcode": "BS6 6QX"},
    {"number": "3274530866", "postcode": "BS6 6QX"},
    {"number": "3437311470", "postcode": "BS6 7QX"},
    {"number": "1696019356", "postcode": "SE1 4HU"},
]

try:
    from glasto._custom.driver import DRIVER_PATH
except Exception as e:
    print(e)
    DRIVER_PATH = os.getenv("CHROMEDRIVER", '/Users/nick/Downloads/chromedriver_107')
    if not DRIVER_PATH:
        raise RuntimeError(
            "Requires chromedriver - set the path via env variable CHROMEDRIVER")

def attemptconnection(client):
    if client.establishconnection(URL, phrases_to_check=[PHRASES_TO_CHECK]):
        print("success")
        if client.submit_registration(REG_DETAILS):
            print("Registration details submission success!")
        client.clickbutton("Click me")
        
# main
try:
    s = gl.Service(DRIVER_PATH)
    c = gl.Twenty23(s, timeout=4, refreshrate=0.000001, verbose=False)
    attemptconnection(c)
    input('...')
except Exception as e:
    print(e)
