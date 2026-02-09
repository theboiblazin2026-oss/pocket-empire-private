#!/usr/bin/env python3
"""
Jarvis LaunchAgent Launcher
This script is designed to be called directly by macOS launchd.
It sets up the environment and runs the Discord bot.
"""
import os
import sys
from dotenv import load_dotenv

# Set working directory to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Load environment variables from .env
load_dotenv() 

# Add the project to path
sys.path.insert(0, SCRIPT_DIR)

# Log startup
print(f"[Launcher] Starting Jarvis...")
print(f"[Launcher] Working directory: {os.getcwd()}")

token = os.getenv('DISCORD_TOKEN')
if not token:
    print("❌ ERROR: DISCORD_TOKEN not found in environment or .env file.")
    sys.exit(1)

print(f"[Launcher] Token found (length: {len(token)})")

# Import and run the bot
exec(open("discord_bot.py").read())
