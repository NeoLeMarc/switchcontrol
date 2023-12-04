#!/usr/bin/env bash
cd ~/switchcontrol/mikrotik
python3 download-config.py all -w
cd ~/switchcontrol-configs
git add **/*.rsc
git commit -m 'backup of config'
git push origin
