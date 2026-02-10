#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.."

echo "🛑 Stopping existing dashboards..."
# Kill ports 8500-8510
for port in {8500..8510}; do
    lsof -ti:$port | xargs kill -9 2>/dev/null
done
sleep 1

echo "🚀 Launching Pocket Empire..."

STREAMLIT_EXEC="/Users/newguy/pocket_venv/bin/streamlit"

# 1. Wealth Manager (8501)
echo "   - Wealth Manager..."
nohup $STREAMLIT_EXEC run pocket_wealth/dashboard.py --server.port 8501 --server.headless true > /dev/null 2>&1 &

# 2. Reminders (8502)
echo "   - Reminders..."
nohup $STREAMLIT_EXEC run pocket_reminders/dashboard.py --server.port 8502 --server.headless true > /dev/null 2>&1 &

# 3. Credit Repair (8503)
echo "   - Credit Repair..."
nohup $STREAMLIT_EXEC run pocket_credit/dashboard.py --server.port 8503 --server.headless true > /dev/null 2>&1 &

# 4. Invoices (8504)
echo "   - Invoices..."
nohup $STREAMLIT_EXEC run pocket_invoices/dashboard.py --server.port 8504 --server.headless true > /dev/null 2>&1 &

# 5. News (8505)
echo "   - News Curator..."
nohup $STREAMLIT_EXEC run pocket_news/dashboard.py --server.port 8505 --server.headless true > /dev/null 2>&1 &

# 6. Router (8506)
echo "   - Route Planner..."
nohup $STREAMLIT_EXEC run pocket_router/dashboard.py --server.port 8506 --server.headless true > /dev/null 2>&1 &

# 7. Leads (8507)
echo "   - Lead Qualifier..."
nohup $STREAMLIT_EXEC run pocket_leads/dashboard.py --server.port 8507 --server.headless true > /dev/null 2>&1 &

# 8. Rates (8508)
echo "   - Rate Negotiator..."
nohup $STREAMLIT_EXEC run pocket_rates/dashboard.py --server.port 8508 --server.headless true > /dev/null 2>&1 &

# 9. Compliance (8509)
echo "   - Compliance Officer..."
nohup $STREAMLIT_EXEC run pocket_compliance/dashboard.py --server.port 8509 --server.headless true > /dev/null 2>&1 &

# 10. Pocket Academy (8510)
echo "   - Pocket Academy (React)..."
cd pocket_academy && npm run dev > /dev/null 2>&1 &
cd ..

# 0. THE HUB (8500)
echo "   - THE HUB (Command Center)..."
nohup $STREAMLIT_EXEC run pocket_hub/Home.py --server.port 8500 --server.headless true > /dev/null 2>&1 &

echo "✅ System Active!"
echo "🌍 Open The Hub: http://localhost:8500"
