#!/bin/bash
# Rate Negotiator Launcher
cd /Users/newguy/.gemini/antigravity/playground/shimmering-eagle
if ! lsof -i :8508 > /dev/null 2>&1; then
    /Users/newguy/pocket_venv/bin/streamlit run pocket_rates/dashboard.py --server.port 8508 --server.headless true &
    sleep 3
fi
open http://localhost:8508
