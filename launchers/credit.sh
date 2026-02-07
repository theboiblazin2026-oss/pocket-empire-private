#!/bin/bash
# Credit Repair Launcher
cd /Users/newguy/.gemini/antigravity/playground/shimmering-eagle
if ! lsof -i :8503 > /dev/null 2>&1; then
    /Users/newguy/pocket_venv/bin/streamlit run pocket_credit/dashboard.py --server.port 8503 --server.headless true &
    sleep 3
fi
open http://localhost:8503
