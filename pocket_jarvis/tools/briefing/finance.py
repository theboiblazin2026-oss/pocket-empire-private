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
        import yfinance as yf
        import math
        
        # Fetch S&P 500
        sp500 = yf.Ticker("^GSPC")
        sp_info = sp500.fast_info
        sp_price = sp_info.get('lastPrice') or sp_info.get('regularMarketPrice')
        if sp_price and not math.isnan(sp_price):
            data['sp500'] = f"${sp_price:,.2f}"
        else:
            # Try history as fallback
            hist = sp500.history(period="5d")
            if not hist.empty:
                data['sp500'] = f"${hist['Close'].iloc[-1]:,.2f}"
            else:
                data['sp500'] = "Market Closed"
        
        # Fetch BTC
        btc = yf.Ticker("BTC-USD")
        btc_info = btc.fast_info
        btc_price = btc_info.get('lastPrice') or btc_info.get('regularMarketPrice')
        if btc_price and not math.isnan(btc_price):
            data['btc'] = f"${btc_price:,.2f}"
        else:
            data['btc'] = "N/A"
            
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
