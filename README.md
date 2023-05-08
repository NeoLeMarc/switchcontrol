# switchcontrol
Automation for some common switch types like Mikrotik and Ubiquiti

# Configuration
Create a read-only user on your switches. Configure Create a config.yaml in your home/.config/switchcontrol/config.yaml:

```
auth:
    username: switchcontrol
    password: "your password"
```

Adapt switches.yaml to match your environment - especially the hostnames.

# Usage
## checkintegrity.py
This script fetches VLAN information from all switches. It then checks for all switches configured as neighbors in `switches.yaml`, if
their respective ports have the same vlan configuration. This is actually the main reason I write that tool, because I often had some
mysterious errors that resulted from missing VLANs or not matching PVIDs.

It then also checks all ports that are configured as trunk ports if they have all VLANs configured, that the script encountered when scanning 
the switches. You can exclude certain VLANs (e.g. management VLANs or M-LAG neighbor ports) by configuring them as "special-vlans" in `switches.yaml`.

The script also warns if the current-vlan list is bigger than the static vlan list - this usually means that you forgot to configured untagged vlans on some
ports.

The script also displays VLAN names for each switches to help with debugging.
