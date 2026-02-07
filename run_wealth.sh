#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
streamlit run pocket_wealth/dashboard.py --server.port 8509
