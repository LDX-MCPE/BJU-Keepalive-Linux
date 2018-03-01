#!/usr/bin/env python3

# BJU Proxy Keepalive Script for Linux
# Created By: Luke Darling
# Version: 1.1
# Creation Date: 2/9/2018
# Modification Date: 2/14/2018


# Imports

import sys, time, getpass

import requests
from requests_ntlm import HttpNtlmAuth


# Define variables

username = ""
password = ""

refreshMinutes = 8

loopCount = refreshMinutes
myOldStatus = 0


# Get the username and password

if len(sys.argv) >= 3:
    username = sys.argv[1]
    password = sys.argv[2]
else:
    while username == "":
        username = input("Username: ").strip()
    while password == "":
        password = getpass.getpass("Password: ").strip()

# Log out the user
requests.get("http://proxylogout.bju.edu/")

print("Starting BJU proxy keepalive script...")

# Loop infinitely
while True:
    try:
        # Check the status
        req = requests.get("http://keepalive.bju.net/proxycheck")
        myStatus = req.status_code

        # If required, attempt to authenticate
        if myStatus != myOldStatus or loopCount >= refreshMinutes:
            loopCount = 0

            if myStatus == 404:
                requests.get("https://proxy1.bju.edu:4433/", auth=HttpNtlmAuth("BJU.EDU\\" + username, password))


            elif myStatus == 504:
                requests.get("https://proxy2.bju.edu:4433/", auth=HttpNtlmAuth("BJU.EDU\\" + username, password))

        # Update loop variables and sleep for 60 seconds
        myOldStatus = myStatus
        loopCount += 1
        time.sleep(10)
    except:
        time.sleep(10)
        continue
