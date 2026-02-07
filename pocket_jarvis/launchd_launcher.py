#!/usr/bin/env python3
"""
Jarvis LaunchAgent Launcher
This script is designed to be called directly by macOS launchd.
It sets up the environment and runs the Discord bot.
"""
import os
import sys

# Set working directory
os.chdir("/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_jarvis")

# Set environment variables (from .env file content)
os.environ["DISCORD_TOKEN"] = "MTQ2NzcyNzExNTYzMjkwNjM5MQ.Ga9W_L.iczek7nxFyeU5gp5ITL-1wTCr_B-Zr17Jg2Evw"
os.environ["DISCORD_USER_ID"] = "780918840154521650"

# Add the project to path
sys.path.insert(0, "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_jarvis")

# Log startup
print(f"[Launcher] Starting Jarvis...")
print(f"[Launcher] Working directory: {os.getcwd()}")
print(f"[Launcher] Token length: {len(os.environ.get('DISCORD_TOKEN', ''))}")

# Import and run the bot
exec(open("discord_bot.py").read())
