#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import librouteros
import yaml
import switch
from common import *

class Commands(object):
    def __init__(self, config):
        self.config = config
        self.switchInfo = switch.SwitchInfo(config)
        self.switchInfo.init()

        site = self.config['site']

        ## Load switches from yaml
        with open('../switches.yaml', 'r') as stream:
            self.switches = yaml.safe_load(stream)[site]

    def getConfig(self, switchName):
        # self.switches is a list of dictionaries
        # we need to extract that dictionary where the key 'name' is equal to switchName
        # then we can get the hostname from that dictionary
        # we do this in one line using a list comprehension
        switch = [switch for switch in self.switches['switches'] if switch['name'] == switchName][0]

        # config export via API is not possible so we will use SSH
        # we will use the python library paramiko
        import paramiko
        # create a new SSH client
        ssh = paramiko.SSHClient()
        # add the switch to the list of known hosts
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect to the switch
        ssh.connect(switch['hostname'], username=self.config['auth']['username'], password=self.config['auth']['password'], allow_agent=False, look_for_keys=False)
        # execute the command
        stdin, stdout, stderr = ssh.exec_command('/export')
        # read the output
        config = stdout.read().decode('utf-8')
        # close the connection
        ssh.close()
        # return the config
        return config

    def _execute(self, switchName, cmd):
        switch = [switch for switch in self.switches['switches'] if switch['name'] == switchName][0]
        connection = librouteros.connect(
            host=switch['hostname'],
            username=self.config['auth']['username'],
            password=self.config['auth']['password'],
            use_ssl=True
        )
        result = connection(cmd=cmd)
        return result 

    def _getConnection(self, switchName):
        switch = [switch for switch in self.switches['switches'] if switch['name'] == switchName][0]
        connection = librouteros.connect(
            host=switch['hostname'],
            username=self.config['auth']['username'],
            password=self.config['auth']['password'],
            use_ssl=True
        )
        return connection

    def getSwitches(self):
        return self.switches['switches']
