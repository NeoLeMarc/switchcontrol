#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import formating and priting functions
from common import *

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

#print(vlanInfo.getPortVlans('ka-10ge-sw1', 'sfp-sfpplus1'))
#print(switchInfo.getNeighbors('ka-10ge-sw1'))

def compareVlans(localVlanInfo, remoteVlanInfo):
    localVlans = localVlanInfo['tagged'] + localVlanInfo['untagged']
    remoteVlans = remoteVlanInfo['tagged'] + remoteVlanInfo['untagged']

    # Find common vlans
    commonVlans = []
    for vlan in localVlans:
        if vlan in remoteVlans:
            commonVlans.append(vlan)

    # Find vlans that are in local but not remote
    localOnlyVlans = []
    for vlan in localVlans:
        if vlan not in remoteVlans:
            localOnlyVlans.append(vlan)

    # Find vlans that are in remote but not local
    remoteOnlyVlans = []
    for vlan in remoteVlans:
        if vlan not in localVlans:
            remoteOnlyVlans.append(vlan)

    return {'common': commonVlans,
            'local-only': localOnlyVlans,
            'remote-only': remoteOnlyVlans
            }

def printNeighbor(switchName, neighbor):
    print(" Neighbor: {}".format(neighbor['name']))
    print("  Local Port: {}".format(neighbor['local-port']))
    print("  Remote Port: {}".format(neighbor['remote-port']))

    localVlanInfo = vlanInfo.getPortVlans(switchName, neighbor['local-port'])
    remoteVlanInfo = vlanInfo.getPortVlans(neighbor['name'], neighbor['remote-port'])
    print("  LOCAL:  " + str(localVlanInfo))
    print("  REMOTE: " + str(remoteVlanInfo))

    vlanComparison = compareVlans(localVlanInfo, remoteVlanInfo)
    print("  Common: " + str(vlanComparison['common']))
    print("  Local Only: " + str(vlanComparison['local-only']))
    print("  Remote Only: " + str(vlanComparison['remote-only']))

    if len(vlanComparison['local-only']) > 0:
        print("Warning: VLANs on local port but not remote port")

    if len(vlanComparison['remote-only']) > 0:
        print("Warning: VLANs on remote port but not local port")

    # warn if pvid mismatch
    if localVlanInfo['pvid'] != remoteVlanInfo['pvid']:
        print("Warning: PVID mismatch")

    print()

def printTrunkPort(switchName, trunkPort):
    print(" Trunk Port: {}".format(trunkPort))
    localVlanInfo = vlanInfo.getPortVlans(switchName, trunkPort['port'])
    print("  VLANs:  " + str(localVlanInfo))

    vlanComparison = compareVlans(localVlanInfo, {'tagged' : vlanInfo.getNonSpecialVlans(), 'untagged' : []})

    if len(vlanComparison['local-only']) > 0 and len([vlan for vlan in vlanComparison['local-only'] if vlan not in vlanInfo.getSpecialVlans()]) > 0:
        printWarning("  Warning: unknown VLANs on trunk: {}".format(vlanComparison['local-only']))

    if len(vlanComparison['remote-only']) > 0:
        printError("  ERROR: VLANS {} missing from trunk port {} on switch {}".format(vlanComparison['remote-only'], trunkPort['port'], switchName))

    print()

def printVlanNames(switchName):
    print("VLAN names on switch {}".format(switchName))
    vlans = vlanInfo.getVlanNames(switchName)
    for vlanId in sorted(vlans.keys()):
        print("  VLAN {}: {}".format(vlanId, vlans[vlanId]))

for switchName in switchInfo.getSwitchNames():
    printHeadline("Switch: {}".format(switchName))
    neighbors = switchInfo.getNeighbors(switchName)
    trunkPorts = switchInfo.getTrunkPorts(switchName)

    print("VLAN names:")
    printVlanNames(switchName)

    print("Neighbors:")
    for neighbor in neighbors:
        printNeighbor(switchName, neighbor)

    print("Trunk Ports:")
    for trunkPort in trunkPorts:
        printTrunkPort(switchName, trunkPort)
    print()

