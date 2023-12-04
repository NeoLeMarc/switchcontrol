#!/usr/bin/env bash
cd mikrotik
python3 download-config.py all -w
cd ~/switchcontrol-configs
git add **/*.rsc
git commit -m "backup of config - created from host $HOSTNAME"
git pull
git push origin
