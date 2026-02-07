#!/bin/bash

# Navigate to project root (2 levels up from script if it was inside tools, but this script is in pocket_jarvis)
# Actually, let's assume this script is in pocket_jarvis/
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$DIR")"

cd "$PROJECT_ROOT"

echo "⏰ Jarvis Check Started at $(date)" >> "$DIR/briefing.log"

# --- SMART DAILY CHECK ---
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$DIR/last_briefing.log"

if [ -f "$LOG_FILE" ]; then
    LAST_RUN=$(cat "$LOG_FILE")
    if [ "$LAST_RUN" == "$TODAY" ]; then
        echo "✅ Already briefed today ($TODAY). Skipping." >> "$DIR/briefing.log"
        exit 0
    fi
fi
# -------------------------

# Run Python Script
# Use the local venv in project root
PYTHON_EXEC="$PROJECT_ROOT/.venv/bin/python3"

echo "🚀 Generating Briefing..." >> "$DIR/briefing.log"
$PYTHON_EXEC "$DIR/run_briefing.py" >> "$DIR/briefing.log" 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Briefing Sent Successfully." >> "$DIR/briefing.log"
    echo "$TODAY" > "$LOG_FILE"
else
    echo "❌ Briefing Failed." >> "$DIR/briefing.log"
fi
