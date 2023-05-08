#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml

class SwitchInfo(object):
    def __init__(self, config):
        self.config = config
        self.switchDB = {}

        ## load switches from yaml
        with open('../switches.yaml', 'r') as stream:
            self.switches = yaml.safe_load(stream)

    def init(self):
        self._buildSwitchDB()

    def _buildSwitchDB(self):
        for switch in self.switches['switches']:
            entry = {'hostname': switch['hostname'],
                     'neighbors' : switch['neighbors'],
                     'trunk-ports' : switch['trunk-ports']}
            self.switchDB[switch['name']] = entry

    def getSwitchNames(self):
        return self.switchDB.keys()

    def getNeighbors(self, switchname):
        neighbors = self.switchDB[switchname]['neighbors']

        neighborInfos = []
        for neighbor in neighbors:

            # Get remote port from switchDB
            remoteSwitch = self.switchDB[neighbor['name']]
            
            for remoteNeighbor in remoteSwitch['neighbors']:
                if remoteNeighbor['name'] == switchname:
                    remotePort = remoteNeighbor['port']
                    break

            neighborInfo = {'name': neighbor['name'],
                            'local-port': neighbor['port'],
                            'remote-port': remotePort
                            }
            neighborInfos.append(neighborInfo)

        return neighborInfos

    def getTrunkPorts(self, switchname):
        trunkPorts = self.switchDB[switchname]['trunk-ports']
        return trunkPorts
