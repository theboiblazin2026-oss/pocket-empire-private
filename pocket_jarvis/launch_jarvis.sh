#!/bin/bash
# Jarvis LaunchAgent Wrapper
# This script is called by macOS LaunchAgent on login

echo "[$(date)] Starting Jarvis wrapper script..."

cd /Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_jarvis || { echo "Failed to cd"; exit 1; }

echo "[$(date)] Working directory: $(pwd)"
echo "[$(date)] Sourcing .env file..."

# Source the .env file manually for environment variables
if [ -f .env ]; then
    export DISCORD_TOKEN=$(grep DISCORD_TOKEN .env | cut -d '=' -f2)
    export DISCORD_USER_ID=$(grep DISCORD_USER_ID .env | cut -d '=' -f2)
    echo "[$(date)] DISCORD_TOKEN length: ${#DISCORD_TOKEN}"
    echo "[$(date)] DISCORD_USER_ID: $DISCORD_USER_ID"
else
    echo "[$(date)] ERROR: .env file not found!"
    exit 1
fi

echo "[$(date)] Starting Python script..."
exec /Users/newguy/.gemini/antigravity/playground/shimmering-eagle/.venv/bin/python3 discord_bot.py
