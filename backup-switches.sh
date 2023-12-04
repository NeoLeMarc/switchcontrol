#!/usr/bin/env bash
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa_unattended
cd mikrotik
python3 download-config.py all -w
cd ~/switchcontrol-configs
git add **/*.rsc
git commit -m "backup of config - created from host $HOSTNAME"
git pull
git push origin
git push github
