import subprocess
import sys

def run_applescript(script):
    try:
        # Run osascript command
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error: {result.stderr}")
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mac_control.py <command> [args...]")
        print("Examples:")
        print("  python3 mac_control.py spotify_play")
        print("  python3 mac_control.py open_url https://google.com")
        print("  python3 mac_control.py set_volume 50")
        exit(1)

    command = sys.argv[1]

    if command == "spotify_play":
        print("🎵 Playing Spotify...")
        run_applescript('tell application "Spotify" to play')
    
    elif command == "spotify_pause":
        print("Unknown command. Add more to mac_control.py!")
        run_applescript('tell application "Spotify" to pause')

    elif command == "spotify_next":
         print("⏭️ Next Track...")
         run_applescript('tell application "Spotify" to next track')

    elif command == "open_url":
        url = sys.argv[2] if len(sys.argv) > 2 else "https://google.com"
        print(f"🌐 Opening {url}...")
        script = f'open location "{url}"'
        run_applescript(script)
        
    elif command == "set_volume":
        vol = sys.argv[2] if len(sys.argv) > 2 else "50"
        print(f"🔊 Setting volume to {vol}%...")
        script = f'set volume output volume {vol}'
        run_applescript(script)
    
    elif command == "say":
        text = " ".join(sys.argv[2:])
        run_applescript(f'say "{text}"')

    else:
        print(f"Unknown command '{command}'. You can add custom AppleScripts to mac_control.py!")
