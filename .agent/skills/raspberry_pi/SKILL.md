---
name: Raspberry Pi
description: Linux, GPIO, Python scripts, networking
---

# Raspberry Pi Skill

## GPIO with Python

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

try:
    while True:
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
finally:
    GPIO.cleanup()
```

## GPIO Pinout

| BCM | Physical | Function |
|-----|----------|----------|
| GPIO2 | 3 | I2C SDA |
| GPIO3 | 5 | I2C SCL |
| GPIO17 | 11 | General |
| GPIO18 | 12 | PWM |

## Common Commands

```bash
# System info
cat /proc/cpuinfo
vcgencmd measure_temp

# Network
hostname -I
sudo raspi-config

# Update
sudo apt update && sudo apt upgrade
```

## Running Scripts on Boot

```bash
# Add to /etc/rc.local (before exit 0)
python3 /home/pi/myscript.py &

# Or use systemd service
sudo systemctl enable myservice
```

## Project Ideas

- Home automation controller
- Network-attached storage (NAS)
- Pi-hole ad blocker
- Media server (Plex, Kodi)
- Retro gaming console

## When to Apply
Use when building Raspberry Pi projects or home automation.
