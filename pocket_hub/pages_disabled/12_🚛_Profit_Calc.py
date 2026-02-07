import streamlit as st
import random
import sys
import os

# Add parent directory to path so we can import if needed (though this is standalone logic)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# US States for dropdown
US_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# Major trucking cities
MAJOR_CITIES = [
    "Atlanta", "Austin", "Baltimore", "Birmingham", "Boston", "Charlotte",
    "Chicago", "Cincinnati", "Cleveland", "Columbus", "Dallas", "Denver",
    "Detroit", "El Paso", "Fort Worth", "Fresno", "Houston", "Indianapolis",
    "Jacksonville", "Kansas City", "Las Vegas", "Los Angeles", "Louisville",
    "Memphis", "Miami", "Milwaukee", "Minneapolis", "Nashville", "New Orleans",
    "New York", "Oakland", "Oklahoma City", "Omaha", "Orlando", "Philadelphia",
    "Phoenix", "Pittsburgh", "Portland", "Raleigh", "Sacramento", "Salt Lake City",
    "San Antonio", "San Diego", "San Francisco", "Seattle", "St. Louis", "Tampa", "Tucson"
]

def get_market_rate(origin, destination, trailer_type):
    """
    Ported from Dispatch App (marketRateService.js)
    Mock logic based on region.
    """
    base_rate = 2.20

    # Competitive Outbound (Lower Rates)
    if any(s in origin for s in ['CA', 'TX', 'IL', 'GA']):
        base_rate -= 0.30
    
    # Hard to Cover Inbound (Higher Rates)
    if any(s in destination for s in ['ND', 'MT', 'WY', 'SD']):
        base_rate += 0.80

    if trailer_type == 'Reefer':
        base_rate += 0.40
    if trailer_type == 'Flatbed':
        base_rate += 0.50

    # Small variance
    variance = (random.random() * 0.40) - 0.20
    return round(base_rate + variance, 2)

def get_lane_score():
    """Ported from Dispatch App: Random 6-10 score"""
    return random.randint(6, 10)

def main():
    st.set_page_config(layout="wide", page_title="Profit Calculator", page_icon="🚛")
    
    st.title("🚛 Smart Dispatch: Profit Calculator")
    st.markdown("Analyze load profitability based on rate, distance, and market conditions.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Load Details")
        rate = st.number_input("Total Rate ($)", min_value=0.0, value=1200.0, step=50.0)
        distance = st.number_input("Loaded Miles", min_value=1, value=500)
        deadhead = st.slider("Deadhead Miles", 0, 200, 50)
        
        # Origin with city dropdown + state dropdown
        st.markdown("**Origin**")
        o_col1, o_col2 = st.columns([2, 1])
        origin_city = o_col1.selectbox("City", MAJOR_CITIES, index=MAJOR_CITIES.index("Dallas"), key="origin_city")
        origin_state = o_col2.selectbox("State", US_STATES, index=US_STATES.index("TX"), key="origin_state")
        origin = f"{origin_city}, {origin_state}"
        
        # Destination with city dropdown + state dropdown
        st.markdown("**Destination**")
        d_col1, d_col2 = st.columns([2, 1])
        dest_city = d_col1.selectbox("City", MAJOR_CITIES, index=MAJOR_CITIES.index("Phoenix"), key="dest_city")
        dest_state = d_col2.selectbox("State", US_STATES, index=US_STATES.index("AZ"), key="dest_state")
        destination = f"{dest_city}, {dest_state}"
        
        trailer_type = st.selectbox("Trailer Type", ["Van", "Reefer", "Flatbed"])
        
        st.divider()
        st.markdown("**Vehicle Settings**")
        mpg = st.number_input("MPG", min_value=3.0, max_value=15.0, value=6.5, step=0.5)
        fuel_price = st.number_input("Diesel ($/gal)", min_value=2.0, max_value=8.0, value=4.15, step=0.05)

    with col2:
        st.subheader("📊 Smart Analysis")
        
        # Core Calculations
        total_miles = distance + deadhead
        
        # RPM Calculations
        loaded_rpm = round(rate / distance, 2) if distance > 0 else 0
        true_rpm = round(rate / total_miles, 2) if total_miles > 0 else 0
        
        # Fuel Calculations
        gallons_needed = total_miles / mpg
        fuel_cost = round(gallons_needed * fuel_price, 2)
        
        # Gross Profit
        gross_profit = round(rate - fuel_cost, 2)
        profit_margin = round((gross_profit / rate) * 100, 1) if rate > 0 else 0
        
        # Market Analysis
        market_rate = get_market_rate(origin, destination, trailer_type)
        lane_score = get_lane_score()
        market_diff = round(true_rpm - market_rate, 2)
        
        recommendation = "Book It" if true_rpm > market_rate else "Negotiate"
        
        # === ROW 1: RPM Metrics ===
        st.markdown("**💰 Rate Per Mile**")
        rpm1, rpm2 = st.columns(2)
        rpm1.metric("Loaded Only RPM", f"${loaded_rpm:.2f}")
        rpm2.metric("True RPM (w/ Deadhead)", f"${true_rpm:.2f}", delta=f"{true_rpm - loaded_rpm:.2f} impact")
        
        st.divider()
        
        # === ROW 2: Cost & Profit ===
        st.markdown("**⛽ Fuel & Profit**")
        cost1, cost2, cost3 = st.columns(3)
        cost1.metric("Fuel Cost", f"${fuel_cost:.2f}", delta=f"{gallons_needed:.1f} gal")
        cost2.metric("Gross Profit", f"${gross_profit:.2f}", delta=f"{profit_margin}% margin", delta_color="normal")
        cost3.metric("Lane Score", f"{lane_score}/10")
        
        st.divider()
        
        # === ROW 3: Market Comparison ===
        st.markdown("**📈 Market Analysis**")
        mkt1, mkt2 = st.columns(2)
        mkt1.metric("Market Avg", f"${market_rate:.2f}/mi")
        mkt2.metric("Your Rate vs Market", f"${market_diff:.2f}", delta_color="normal")

        st.divider()

        # Recommendation Card
        if recommendation == "Book It":
            st.success(f"### ✅ Recommendation: {recommendation}")
            st.markdown(f"Rate is **${market_diff} above** market. Profit: **${gross_profit}**")
        else:
            st.warning(f"### ⚠️ Recommendation: {recommendation}")
            st.markdown(f"Rate is **${abs(market_diff)} below** market. Consider negotiating **+${abs(market_diff)*total_miles:.0f}**")

        # Data Visualization placeholder
        st.info("💡 Tip: Use the 'Rate Negotiator' agent to generate a script if you need to negotiate higher.")

if __name__ == "__main__":
    main()
