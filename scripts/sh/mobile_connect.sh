#!/bin/bash
# mobile_connect.sh
# Establishes a secure tunnel for Mobile Access using Cloudflare

# Kill any existing tunnel
pkill -f "cloudflared tunnel"
pkill -f "ssh -R 80:localhost:8500"

# Output file for the URL
OUTPUT_FILE="mobile_url.txt"
echo "Starting tunnel..." > $OUTPUT_FILE

# Start Cloudflare tunnel (no login needed for quick tunnels)
# This creates a temporary public URL that forwards to localhost:8500
nohup cloudflared tunnel --url http://localhost:8500 > $OUTPUT_FILE 2>&1 &

echo "Tunnel process started. Check UI for URL."
