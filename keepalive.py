#!/usr/bin/env python3

# BJU Proxy Keepalive Script for Linux
# Created By: Luke Darling
# Version: 1.0
# Creation Date: 2/9/2018


# Imports

import sys, time, getpass


# You must install `requests` module using `pip3 install requests`

import requests
from requests.auth import HTTPBasicAuth


# Define variables

username = ""
password = ""

refreshMinutes = 8

loopCount = refreshMinutes
myOldStatus = 0


# Get the username and password

if len(sys.argv) >= 3:
    username = sys.argv[1].strip()
    password = sys.argv[2].strip()
else:
    while username == "":
        username = input("Username: ")
    while password == "":
        password = getpass.getpass("Password: ")
    print("")

# Log out the user
requests.get("http://proxylogout.bju.edu/")

print("Starting BJU proxy keepalive script...")

# Loop infinitely
while True:

    # Check the status
    req = requests.get("http://keepalive.bju.net/proxycheck")
    myStatus = req.status_code

    # If required, attempt to authenticate
    if myStatus != myOldStatus or loopCount >= refreshMinutes:
        loopCount = 0

        if myStatus == 404:
            requests.get("https://proxy1.bju.edu:4433/", auth=(username, password), params={"cfru":"aHR0cHM6Ly9wcm94eTEuYmp1LmVkdS8="})

        elif myStatus == 504:
            requests.get("https://proxy2.bju.edu:4433/", auth=(username, password), params={"cfru":"aHR0cHM6Ly9wcm94eTIuYmp1LmVkdS8="})

    # Update loop variables and sleep for 60 seconds
    myOldStatus = myStatus
    loopCount += 1
    time.sleep(60)