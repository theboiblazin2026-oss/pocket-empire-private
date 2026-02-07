import psutil
import subprocess
import re

def get_system_health():
    """
    Returns a dict of system stats: CPU, RAM, Disk, WiFi, Bluetooth.
    """
    health = {}

    # 1. Basic Resource Usage (psutil)
    health['cpu_percent'] = psutil.cpu_percent(interval=1)
    health['ram_percent'] = psutil.virtual_memory().percent
    health['disk_percent'] = psutil.disk_usage('/').percent

    # 2. WiFi Status (macOS specific)
    try:
        # The 'airport' utility is hidden in macOS
        airport_cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
        result = subprocess.run(airport_cmd, shell=True, capture_output=True, text=True)
        
        if "AirPort: Off" in result.stdout:
            health['wifi_status'] = "🔴 OFF"
            health['wifi_ssid'] = "N/A"
        else:
            # Extract SSID
            match = re.search(r"SSID: (.+)", result.stdout)
            if match:
                health['wifi_status'] = "🟢 Connected"
                health['wifi_ssid'] = match.group(1).strip()
            else:
                health['wifi_status'] = "🟡 On (Disconnected)"
                health['wifi_ssid'] = "None"
    except Exception as e:
        health['wifi_status'] = f"❌ Error: {e}"

    # 3. Bluetooth Status (macOS specific)
    try:
        # system_profiler is detailed but slow. We'll use a quicker check if possible, 
        # but SP is the most reliable native way.
        # checking controller power state
        bt_cmd = "system_profiler SPBluetoothDataType"
        result = subprocess.run(bt_cmd, shell=True, capture_output=True, text=True)
        
        # Simple string check for State
        if "State: On" in result.stdout or "Power: On" in result.stdout:
             health['bt_status'] = "🟢 ON"
        elif "State: Off" in result.stdout or "Power: Off" in result.stdout:
             health['bt_status'] = "🔴 OFF"
        else:
             health['bt_status'] = "❓ Unknown"
             
        # Count connected devices
        devices = result.stdout.count("Connected: Yes")
        health['bt_devices'] = devices

    except Exception as e:
        health['bt_status'] = f"❌ Error: {e}"

    return health

if __name__ == "__main__":
    print(get_system_health())
