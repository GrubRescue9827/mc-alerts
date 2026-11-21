# mc-alerts
A simple NTFY alert script for Minecraft Servers that relies on [StatusPing](https://gist.github.com/ewized/97814f57ac85af7128bf) instead of using latency to the host via the `ping` shell command.
This fixes issues with Minecraft servers behind reverse-proxies, since we want to measure RTT to the Minecraft server, not just to the reverse proxy.

This project is designed to be as simple as possible. Originally written in BASH (not public), this port is significantly faster without as many bugs.
No AI was used to write this code.

# Usage:
Can be ran in a shell like so:

```bash
python3 mc-alerts.py
```

Or as a systemd service using the provided `.service` file.
