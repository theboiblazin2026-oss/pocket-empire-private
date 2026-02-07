#!/bin/bash
# Stop Jarvis
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$DIR/jarvis.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        rm "$PID_FILE"
        echo "🛑 Jarvis stopped (PID: $PID)"
    else
        rm "$PID_FILE"
        echo "⚠️ Jarvis was not running (stale PID file removed)"
    fi
else
    echo "ℹ️ No PID file found. Jarvis may not be running."
fi
