#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Download config from Mikrotik switch

# Parse arguments
import argparse
parser = argparse.ArgumentParser()
# Get name of switch from arugments
parser.add_argument("switch", help="Name of switch")
# Write to disk?
parser.add_argument("-w", "--write", help="Write to disk", action="store_true")
args = parser.parse_args()

# Get switch name from arguments
switchName = args.switch

# import formating and priting functions
from common import *

# Read username and password from config file
import yaml

# Resolve path to config file
import os
path = os.path.expanduser("~/.config/switchcontrol/config.yaml")
with open(path, 'r') as stream:
    config = yaml.safe_load(stream)
site = config['site']

# Import commands
from commands import Commands
commands = Commands(config)

if switchName != "all":
    config = commands.getConfig(switchName)
    print(config)
    # Write to disk?
    # File path is ~/switchcontrol-configs/<site>/<switchname>.rsc
    if args.write:
        print("Writing config to disk")
        print("======================================")
        path = os.path.expanduser("~/switchcontrol-configs/" + site + "/" + switchName + ".rsc")
        with open(path, 'w') as file:
            file.write(config)
        print("Done")
else:
    config = ""
    for switch in commands.getSwitches():
        print("Downloading config from switch: " + switch['name'])
        print("======================================")
        config = commands.getConfig(switch['name'])
        print(config)

        # Write to disk?
        # File path is ~/switchcontrol-configs/<site>/<switchname>.rsc
        if args.write:
            print("Writing config to disk")
            print("======================================")
            path = os.path.expanduser("~/switchcontrol-configs/" + site + "/" + switch['name'] + ".rsc")
            with open(path, 'w') as file:
                file.write(config)
            print("Done")
        print("======================================")
        print("\n\n")


