from selenium.webdriver.common.keys import Keys as Keys

from glasto.client import Client, RefresherClient, ScoutClient, Service
from glasto.twenty19 import Twenty19, Twenty19WithKillSwitch
from glasto.twenty20 import Twenty20
from glasto.twenty23 import Twenty23
from glasto.util import *

try:
    from glasto._custom.driver import DRIVER_PATH
except:
    import os
    DRIVER_PATH = os.getenv("CHROMEDRIVER", '/Users/nick/Downloads/chromedriver_107')
    if not DRIVER_PATH:
        raise RuntimeError(
            "Requires chromedriver - set the path via env variable CHROMEDRIVER")
