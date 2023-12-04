#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import librouteros
import yaml
import switch
from common import *

class VlanInfo(object):
    def __init__(self, config):
        self.config = config
        self.vlanDB = {}
        self.switchInfo = switch.SwitchInfo(config)
        self.switchInfo.init()

        site = self.config['site']

        ## load switches from yaml
        with open('../switches.yaml', 'r') as stream:
            self.switches = yaml.safe_load(stream)[site]

    def init(self):
        self._buildVlanDB()

    def _getVlans(self, host):
        # Get list of VLANs
        connection = librouteros.connect(
            host=host,
            username=self.config['auth']['username'],
            password=self.config['auth']['password'],
            use_ssl=True
        )

        vlans = connection(cmd='/interface/bridge/vlan/print')
        return vlans

    def _getPvids(self, host):
        # Get port information from switch
        connection = librouteros.connect(
            host=host,
            username=self.config['auth']['username'],
            password=self.config['auth']['password'],
            use_ssl=True
        )

        ports = connection(cmd='/interface/bridge/port/print')

        # Extract pvids from ports
        pvids = {}
        for port in ports:
            pvids[port['interface']] = port['pvid']

        return pvids

    def _getVlanNames(self, host):
        # Get list of VLANs
        connection = librouteros.connect(
            host=host,
            username=self.config['auth']['username'],
            password=self.config['auth']['password'],
            use_ssl=True
        )

        vlans = connection(cmd='/interface/vlan/print')

        # Extract vlan names from vlans
        vlanNames = {}
        for vlan in vlans:
            vlanNames[vlan['vlan-id']] = vlan['name']

        return vlanNames

    def _buildVlanDB(self):
        # Get list of vlans from each switch
        for switch in self.switches['switches']:
            vlans = self._getVlans(switch['hostname'])
            switchVlans = [vlan for vlan in vlans]
            pvids = self._getPvids(switch['hostname'])
            vlanNames = self._getVlanNames(switch['hostname'])

            vlanTemp = {}

            for vlan in switchVlans:
                taggedPorts = vlan['tagged'].split(',')
                untaggedPorts = vlan['untagged'].split(',')
                currentTaggedPorts = vlan['current-tagged'].split(',')
                currentUntaggedPorts = vlan['current-untagged'].split(',')

                if len(currentTaggedPorts) > len(taggedPorts):
                    printWarning("Warning: Current tagged ports is greater than tagged ports for vlan " + str(vlan['vlan-ids']) + " on switch " + switch['name'])
                    print("Current tagged ports: " + str(currentTaggedPorts))

                if len(currentUntaggedPorts) > len(untaggedPorts):
                    printWarning("Warning: Current untagged ports is greater than untagged ports for vlan " + str(vlan['vlan-ids']) + " on switch " + switch['name'])
                    print("Current untagged ports: " + str(currentUntaggedPorts))

                vlanTemp[vlan['vlan-ids']] = {
                    'tagged': taggedPorts,
                    'untagged': untaggedPorts,
                    'current-tagged': currentTaggedPorts,
                    'current-untagged': currentUntaggedPorts

                }

            self.vlanDB[switch['name']] = {'vlans' : vlanTemp, 'pvids': pvids, 'vlanNames': vlanNames}

    def getPortVlans(self, switchname, port):
        # Get list of vlans from switch
        vlanDB = self.vlanDB[switchname]
        vlans = vlanDB['vlans']
        pvids = vlanDB['pvids']

        # Find vlans that are tagged on port
        taggedVlans = []
        for vlan in vlans:
            if port in vlans[vlan]['tagged']:
                taggedVlans.append(vlan)

        # Find vlans that are untagged on port
        untaggedVlans = []
        for vlan in vlans:
            if port in vlans[vlan]['untagged']:
                untaggedVlans.append(vlan)

        if pvids[port] not in untaggedVlans:
            printWarning("Warning: PVID " + str(pvids[port]) + " is not in untagged vlans for port " + port + " on switch " + switchname)

        return {
            'tagged': sorted(taggedVlans),
            'untagged': sorted(untaggedVlans),
            'pvid' :pvids[port]
        }

    def getVlanNames(self, switchname):
        return self.vlanDB[switchname]['vlanNames']

    def getAllVlans(self):
        vlanList = [switch['vlans'].keys() for switch in self.vlanDB.values()] 
        # Unify list of lists into list
        vlanList = list(set([item for sublist in vlanList for item in sublist]))
        return vlanList

    def getNonSpecialVlans(self):
        specialVlans = self.switchInfo.getSpecialVlans()
        allVlans = self.getAllVlans()
        nonSpecialVlans = [vlan for vlan in allVlans if vlan not in specialVlans]
        return nonSpecialVlans

    def getSpecialVlans(self):
        specialVlans = self.switchInfo.getSpecialVlans()
        return specialVlans

