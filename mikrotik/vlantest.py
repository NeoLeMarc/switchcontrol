#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read username and password from config file
import yaml

# Resolve path to config file
import os
path = os.path.expanduser("~/.config/switchcontrol/config.yaml")
with open(path, 'r') as stream:
    config = yaml.safe_load(stream)

from vlan import VlanInfo
vlanInfo = VlanInfo(config)
vlanInfo.init()

from switch import SwitchInfo
switchInfo = SwitchInfo(config)
switchInfo.init()

print(vlanInfo.getPortVlans('ka-10ge-sw1', 'sfp-sfpplus1'))
print(switchInfo.getNeighbors('ka-10ge-sw1'))
