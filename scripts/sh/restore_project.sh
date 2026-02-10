#!/bin/bash

SOURCE="/Volumes/CeeJay SSD/Projects/PocketEmpire"
DEST="/Users/newguy/Projects/PocketEmpire"
BACKUP="/Users/newguy/Projects/PocketEmpire_Backup_$(date +%Y%m%d_%H%M%S)"

echo "🚀 Starting Project Restoration to Internal Drive..."

# 1. Check if destination exists and backup
if [ -d "$DEST" ]; then
    echo "⚠️  Found existing project at $DEST"
    echo "📦 Moving it to backup: $BACKUP"
    mv "$DEST" "$BACKUP"
fi

# 2. Copy from SSD to Internal
echo "📂 Copying files from SSD to Internal Drive..."
# Use rsync for better handling of .git and large files
rsync -av --progress "$SOURCE/" "$DEST/"

# 3. Validation
if [ -d "$DEST" ] && [ -d "$DEST/.git" ]; then
    echo "✅ Success! Project restored to $DEST"
    echo "🔓 Full Automation Unlocked."
else
    echo "❌ Error: Migration failed. Please check permissions."
    exit 1
fi
