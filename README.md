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
