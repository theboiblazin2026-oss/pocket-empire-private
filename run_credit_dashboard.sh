#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
streamlit run pocket_credit/dashboard.py --server.port 8503
