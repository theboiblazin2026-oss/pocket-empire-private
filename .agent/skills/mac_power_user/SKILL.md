---
name: Mac Power User
description: Terminal tricks, Automator workflows, and hidden macOS settings
---

# Mac Power User Skill

## Essential Terminal Commands

| Task | Command |
|------|---------|
| Show hidden files | `defaults write com.apple.finder AppleShowAllFiles YES && killall Finder` |
| Flush DNS cache | `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` |
| Keep Mac awake | `caffeinate -d` |
| Screenshot without shadow | `defaults write com.apple.screencapture disable-shadow -bool true` |
| Copy file path | `pbcopy < /path/to/file` |
| Quick Look from terminal | `qlmanage -p file.pdf` |

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Spotlight | ⌘ + Space |
| Force Quit | ⌘ + ⌥ + Esc |
| Screenshot (area) | ⌘ + ⇧ + 4 |
| Screenshot (window) | ⌘ + ⇧ + 4, then Space |
| Lock screen | ⌘ + ⌃ + Q |
| Show desktop | F11 or ⌘ + F3 |
| Switch windows (same app) | ⌘ + ` |

## Automator Recipes

### Resize Images
1. Open Automator → Quick Action
2. Add "Scale Images" action
3. Set percentage/pixels
4. Save → Access via right-click

### Convert to PDF
1. Quick Action workflow
2. "Render PDF Pages as Images" or "Create PDF"

## Hidden Settings

```bash
# Faster dock auto-hide
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0.5
killall Dock

# Expand save dialog by default
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true

# Show full file path in Finder title
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
```

## Disk Cleanup Commands

```bash
# Clear system caches
sudo rm -rf /Library/Caches/*
rm -rf ~/Library/Caches/*

# Clear logs
sudo rm -rf /var/log/*

# Find large files
find ~ -type f -size +500M 2>/dev/null

# Check disk usage
du -sh */ | sort -h
```

## When to Apply
Use when optimizing Mac workflows, automating tasks, or troubleshooting system issues.
