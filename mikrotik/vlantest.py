#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read username and password from config file
import yaml

# Resolve path to config file
import os
path = os.path.expanduser("~/.config/switchcontrol/config.yaml")
with open(path, 'r') as stream:
    config = yaml.safe_load(stream)

# Use mikrotik API to connect to switch
import librouteros
connection = librouteros.connect(
    host=config['switch']['host'],
    username=config['auth']['username'],
    password=config['auth']['password'],
    use_ssl=True
)

# Get list of VLANs
vlans = connection(cmd='/interface/bridge/vlan/print')

for vlan in vlans:
    print(vlan)
