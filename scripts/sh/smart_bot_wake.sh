#!/bin/bash
#
# Smart Bot Wake Script v2
# Monitors iPhone Bluetooth AND WiFi presence to start/stop Discord bot
#
# Phone: CeeJay TheBoi
# Bluetooth: 7C:4B:26:4F:BD:13
#
# Logic: Bot runs when phone is AWAY (not detected)
#        Bot stops when phone is NEARBY (detected via BT or WiFi)
#

PHONE_NAME="CeeJay TheBoi"
PHONE_BT_ADDRESS="7C:4B:26:4F:BD:13"
BOT_DIR="/Users/newguy/.gemini/antigravity/playground/shimmering-eagle"
PYTHON="$BOT_DIR/.venv/bin/python3"
PID_FILE="/tmp/discord_bot.pid"
LOG_FILE="/tmp/smart_bot_wake.log"

# Ensure log file exists
touch "$LOG_FILE"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

is_phone_on_bluetooth() {
    # Check if phone is in Bluetooth device list
    system_profiler SPBluetoothDataType 2>/dev/null | grep -q "$PHONE_NAME"
    return $?
}

is_phone_on_wifi() {
    # Check ARP table for phone's MAC address on local network
    # Or ping phone's hostname if it has a static IP/reservation
    # Try multiple methods:
    
    # Method 1: Check ARP table for any iPhone
    arp -a 2>/dev/null | grep -i "iphone\|ceejay" && return 0
    
    # Method 2: If you know phone's local IP, ping it
    # ping -c 1 -W 1 192.168.1.X > /dev/null 2>&1 && return 0
    
    # Method 3: Scan for phone's WiFi MAC (if known)
    # arp -a | grep -q "WIFI_MAC_ADDRESS" && return 0
    
    return 1
}

is_phone_nearby() {
    # Phone is nearby if detected via EITHER Bluetooth OR WiFi
    if is_phone_on_bluetooth; then
        log "📶 Phone detected via Bluetooth"
        return 0
    fi
    
    if is_phone_on_wifi; then
        log "📶 Phone detected via WiFi"
        return 0
    fi
    
    return 1
}

is_bot_running() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Running
        fi
    fi
    # Also check by process name
    pgrep -f "discord_bot.py" > /dev/null 2>&1
    return $?
}

start_bot() {
    log "📱 Phone LEFT - Starting Discord bot..."
    cd "$BOT_DIR"
    nohup "$PYTHON" discord_bot.py > /tmp/discord_bot.log 2>&1 &
    echo $! > "$PID_FILE"
    log "✅ Bot started with PID: $(cat $PID_FILE)"
}

stop_bot() {
    log "📱 Phone RETURNED - Stopping Discord bot..."
    if [ -f "$PID_FILE" ]; then
        kill "$(cat $PID_FILE)" 2>/dev/null
        rm "$PID_FILE"
    fi
    pkill -f "discord_bot.py" 2>/dev/null
    log "✅ Bot stopped"
}

# Main logic
log "🔍 Checking phone presence..."

if is_phone_nearby; then
    # Phone is here - stop bot if running
    if is_bot_running; then
        stop_bot
    else
        log "📱 Phone nearby - bot already stopped"
    fi
else
    # Phone is away - start bot if not running
    log "📱 Phone NOT detected (away)"
    if ! is_bot_running; then
        start_bot
    else
        log "✅ Bot already running"
    fi
fi
