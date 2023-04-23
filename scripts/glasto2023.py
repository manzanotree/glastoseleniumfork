#!/usr/bin/env python3

import concurrent.futures
import os
import time
from concurrent.futures import FIRST_COMPLETED
from multiprocessing import Pool

import glasto as gl

# incognito??
incognito = True

# disable js??
disablejs = False

# disable images for faster loading?
disableimages = True

# change cache size?
cache = 4096

# try a proxy with "8.8.8.8:88"
proxy = None

# run without browser - kind of pointless but faster.
headless = False

# refresh rate - seconds
refreshrate = 0.05

detach = True

# try one of these URLS
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-deposits/worthy-farm/1300000"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/addregistrations"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020/worthy-farm/1300001"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-ticket-coach-travel-deposits/worthy-farm/1450012"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-ticket-coach-travel-deposits/worthy-farm/1450013"
# DEPOSIT_23_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-ticket-coach-travel/worthy-farm/2500011"
DEPOSIT_23_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-deposits/worthy-farm/2500000"
DEPOSIT_23_URL = (
    "http://localhost:3000/event/glastonbury-2023-deposits/worthy-farm/2500000"
)


PHRASES_TO_CHECK = [gl.Twenty23.REGISTRATION_PHRASE]

# first is lead booker
REG_DETAILS = [
    {"number": "154414413", "postcode": "N7 0DU"},
    {"number": "390811765", "postcode": "N7 0DU"},
    {"number": "3069133115", "postcode": "BS6 6QX"},
    {"number": "3274530866", "postcode": "BS6 6QX"},
    {"number": "3437311470", "postcode": "BS6 7QX"},
    {"number": "1696019356", "postcode": "SE1 4HU"},
]

if len(REG_DETAILS) == 0:
    raise RuntimeError("Must have at least one registration!")

if len(REG_DETAILS) > 6:
    raise RuntimeError("Cannot accept more than 1 + 5 registration details!")


def attemptconnection(client, url):
    if client.establishconnection(url, phrases_to_check=PHRASES_TO_CHECK):
        print("success")
        print(client.attempts)
        try:
            gl.tofile(client.content, "reg_page_2023.html")
        except:
            pass
        if client.submit_registration(REG_DETAILS):
            print("Registration details submission success!")
            # save the html data
            try:
                gl.tofile(client.content, "reg_check_2023.html")
            except:
                pass

            try:
                # then click 'confirm' button and save html data again
                client.clickbutton("Confirm")
                gl.tofile(client.pagesource, "payment_page_2023.html")
            except:
                pass

            # we cannot go beyond this automated,
            # since entering credit cards details automatically
            # is terribly risky.
            # instead leave the page open for us to do that
            # and save the content

            # todo: ????
            return
        else:
            print("Registration details submission failed!")
            # XXX This exit loop might need to be removed
            # if unable to submit the registration details then kill and allow human to take over
            return

    # try again??
    # attemptconnection(client, url)

browsers = 4

def main(dump):
    # main
    try:
        s = gl.Service(gl.DRIVER_PATH)
        c = gl.Twenty23(
            s,
            timeout=4,
            refreshrate=refreshrate,
            verbose=False,
            disablejs=disablejs,
            incognito=incognito,
            disableimages=disableimages,
            cache=cache,
            headless=headless,
            proxy=proxy,
            detach=detach,
        )
        attemptconnection(c, DEPOSIT_23_URL)
    except Exception as e:
        print(e)




if __name__ == "__main__":
    try:
        with Pool(processes=browsers) as p:
            p.map(main, (i for i in range(browsers)))
    except Exception as e:
        print("outer", e)

    # backup sleep
    time.sleep(10000000)  # Hack - leave it open to fill in details
