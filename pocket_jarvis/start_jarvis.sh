#!/bin/bash
# Jarvis Background Launcher
# This script starts Jarvis in the background using nohup

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$DIR")"
VENV="$PROJECT_ROOT/.venv/bin/python3"
BOT_SCRIPT="$DIR/discord_bot.py"
LOG_FILE="$DIR/jarvis.log"
PID_FILE="$DIR/jarvis.pid"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️ Jarvis is already running (PID: $OLD_PID)"
        echo "Use 'kill $OLD_PID' to stop it first."
        exit 1
    fi
fi

# Start Jarvis in background
echo "🚀 Starting Jarvis in background..."
cd "$DIR"
nohup "$VENV" "$BOT_SCRIPT" >> "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "✅ Jarvis started! (PID: $NEW_PID)"
echo "📄 Logs: $LOG_FILE"
echo "🛑 To stop: kill $NEW_PID"
