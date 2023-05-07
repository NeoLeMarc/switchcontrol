#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import librouteros
import yaml

class VlanInfo(object):
    def __init__(self, config):
        self.config = config
        self.vlanDB = {}

        ## load switches from yaml
        with open('../switches.yaml', 'r') as stream:
            self.switches = yaml.safe_load(stream)

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

    def _buildVlanDB(self):
        # Get list of vlans from each switch
        for switch in self.switches['switches']:
            vlans = self._getVlans(switch['hostname'])
            self.vlanDB[switch['name']] = [vlan for vlan in vlans]


