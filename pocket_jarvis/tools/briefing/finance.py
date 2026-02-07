import os
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

def get_finance_brief():
    """
    Fetches market data and checks Daily Budget.
    """
    data = {}
    
    # 1. Market Data (S&P 500, BTC)
    try:
        tickers = ["^GSPC", "BTC-USD"]
        prices = yf.download(tickers, period="1d", progress=False)['Close'].iloc[-1]
        
        data['sp500'] = f"${prices['^GSPC']:.2f}"
        data['btc'] = f"${prices['BTC-USD']:.2f}"
    except Exception as e:
        data['error'] = str(e)
        data['sp500'] = "N/A"
        data['btc'] = "N/A"

    # 2. Daily Budget Goal
    # We read this from .env or default to 100
    try:
        goal = float(os.getenv("DAILY_BUDGET_GOAL", "100.00"))
        # Future: Connect to bank API to get actual spend
        # For now, we display the Target.
        data['budget_goal'] = f"${goal:.2f}"
        data['budget_message'] = "Keep grinding! 💸"
    except:
        data['budget_goal'] = "$100.00"

    return data

if __name__ == "__main__":
    print(get_finance_brief())
