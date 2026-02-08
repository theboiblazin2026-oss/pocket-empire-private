#!/bin/bash

echo "🚀 Starting Deployment for Pocket Empire (Damage Inspector Upgrade)..."

# Navigate to project directory
cd "/Volumes/CeeJay SSD/Projects/PocketEmpire" || exit

# Add all changes
git add .

# Commit
git commit -m "feat: Upgrade Damage Inspector (AI + DB) and Fix News Feed"

# Push to main
echo "☁️ Pushing to GitHub..."
git push origin main

echo "✅ Deployment Process Complete!"
echo "👉 Now: Check Streamlit Cloud to see your update live."
