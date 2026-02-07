#!/bin/bash
# Auto-start Pocket Empire with Cloudflare Tunnel
# This script is called by launchd on wake/login

LOG_FILE="/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/auto_start.log"
PROJECT_DIR="/Users/newguy/.gemini/antigravity/playground/shimmering-eagle"

echo "$(date): Auto-start triggered" >> "$LOG_FILE"

# Wait for network
sleep 5

# Check if already running
if lsof -i:8500 > /dev/null 2>&1; then
    echo "$(date): Hub already running on 8500, skipping" >> "$LOG_FILE"
else
    echo "$(date): Starting Pocket Empire..." >> "$LOG_FILE"
    cd "$PROJECT_DIR"
    /bin/bash "$PROJECT_DIR/start_system.sh" >> "$LOG_FILE" 2>&1
fi

# Start Cloudflare tunnel if not running
if ! pgrep -f "cloudflared.*tunnel" > /dev/null 2>&1; then
    echo "$(date): Starting Cloudflare tunnel..." >> "$LOG_FILE"
    nohup /opt/homebrew/bin/cloudflared tunnel --url http://localhost:8500 > "$PROJECT_DIR/tunnel.log" 2>&1 &
    sleep 10
    # Grab the URL
    TUNNEL_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$PROJECT_DIR/tunnel.log" | head -1)
    if [ -n "$TUNNEL_URL" ]; then
        echo "$TUNNEL_URL" > "$PROJECT_DIR/mobile_url.txt"
        echo "$(date): Tunnel URL: $TUNNEL_URL" >> "$LOG_FILE"
    fi
else
    echo "$(date): Tunnel already running" >> "$LOG_FILE"
fi

echo "$(date): Auto-start complete" >> "$LOG_FILE"
