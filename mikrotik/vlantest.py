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

def getVlans(switch):
    connection = librouteros.connect(
        host=config['switch']['host'],
        username=config['auth']['username'],
        password=config['auth']['password'],
        use_ssl=True
    )

    # Get list of VLANs
    vlans = connection(cmd='/interface/bridge/vlan/print')
    return vlans

# Get neighboring information from yaml
with open('../switches.yaml', 'r') as stream:
    switchconfig = yaml.safe_load(stream)
    switches = switchconfig['switches']

# Get list of vlans from each switch
vlanDB = {}

for switch in switches:
    vlans = getVlans(switch['hostname'])
    vlanDB[switch['name']] = [vlan for vlan in vlans]

for switch in vlanDB:
    print(vlanDB[switch])
