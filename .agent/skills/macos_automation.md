---
name: macos_automation
description: A skill to control the Mac desktop using AppleScript.
---

# Ghost in the Shell 🕹️

This skill allows you to automate macOS applications and system functions using AppleScript.

## Capabilities
1.  **App Control**: Open apps, play music, change volume.
2.  **Browser Control**: Open URLs, read active tabs.
3.  **System**: Create reminders, notifications, or calendar events.

## Prerequisites
- macOS (obviously)
- Permission to control accessibility features (System Settings > Privacy & Security > Accessibility) might be needed for some advanced scripts.

## Usage

### Running an Automation
Run the `mac_control.py` script with a predefined task.

\`\`\`python
# mac_control.py
import subprocess
import sys

def run_applescript(script):
    try:
        # Run osascript command
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error: {result.stderr}")
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mac_control.py <command>")
        print("Commands: spotify_play, open_chrome, set_volume_50")
        exit(1)

    command = sys.argv[1]

    if command == "spotify_play":
        script = 'tell application "Spotify" to play'
        run_applescript(script)
    
    elif command == "spotify_pause":
        script = 'tell application "Spotify" to pause'
        run_applescript(script)

    elif command == "open_browser":
        url = sys.argv[2] if len(sys.argv) > 2 else "https://google.com"
        script = f'open location "{url}"'
        run_applescript(script)
        
    elif command == "set_volume":
        vol = sys.argv[2] if len(sys.argv) > 2 else "50"
        script = f'set volume output volume {vol}'
        run_applescript(script)

    else:
        print("Unknown command. Add more to mac_control.py!")
\`\`\`
