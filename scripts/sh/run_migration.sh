#!/bin/bash
echo "🚀 Pocket Empire Data Migration"
echo "--------------------------------"
echo "This script will migrate your local JSON data to Supabase."
echo "Ensure you have added your SUPABASE_URL and SUPABASE_KEY to .streamlit/secrets.toml"
echo ""
read -p "Press Enter to continue..."

python3 migrate_to_supabase.py
