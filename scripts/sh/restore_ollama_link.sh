#!/bin/bash

# Restore Ollama Link Script
# ------------------------
# This script configures Ollama to use the models stored on your External SSD.

echo "Checking for Ollama..."
if ! [ -d "/Applications/Ollama.app" ]; then
    echo "❌ Ollama is not installed in /Applications."
    echo "Please download and install it from https://ollama.com first."
    exit 1
fi

echo "✅ Ollama found."

echo "Configuring Ollama to use SSD models..."
# Stop Ollama if running
pkill ollama

# Set environment variable for the current user
launchctl setenv OLLAMA_MODELS "/Volumes/CeeJay SSD/Ollama_Models"

echo "✅ Environment variable OLLAMA_MODELS set."

echo "Restarting Ollama..."
open -a Ollama

echo "waiting for Ollama to start..."
sleep 5

echo "Verifying models..."
ollama list

echo "---------------------------------------------------"
echo "If you see your models listed above, you are good to go!"
echo "Note: You may need to restart your AI App (Brain/Antigravity) as well."
