#!/bin/bash
echo "Starting Zero to Hero Curriculum..."
# Navigate to the project directory
cd "$(dirname "$0")"

# Start the dev server in the background
npm run dev &
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Open the browser
open "http://localhost:5173"

# Keep the terminal open so the server keeps running
echo "Server is running! Close this window to stop the app."
wait $SERVER_PID
