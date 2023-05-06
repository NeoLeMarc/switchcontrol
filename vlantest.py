#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
# There is currently a bug in working together with pyasn1 > 0.4.8
# Hotfix: pip3 install pyasn1==0.4.8

# https://www.yaklin.ca/2021/08/25/snmp-queries-with-python.html

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
host = 'ka-10ge-sw.wlan.ka.xcore.net'

SYSNAME = '1.3.6.1.2.1.1.5.0'
snmp_ro_comm = 'public'

# Define a PySNMP CommunityData object
auth = cmdgen.CommunityData(snmp_ro_comm)

# Define the CommandGenerator
cmdGen = cmdgen.CommandGenerator()

# Query a network device using the getCmd() function, providing the auth object,
# a UDP transport, our OID for SYSNAME and don't lookup the OID in PySNMP's MIB's
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((host, 161)),
    cmdgen.MibVariable(SYSNAME),
    lookupNames=False)

# Check wether there was an error querying the device
if errorIndication:
    sys.exit()

for oid, val in varBinds:
    print(oid.prettyPrint(), val.prettyPrint())

