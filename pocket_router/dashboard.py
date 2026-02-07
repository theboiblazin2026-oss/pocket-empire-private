import streamlit as st
import sys
import os
import folium
from streamlit_folium import st_folium
import requests
import urllib.parse
import polyline

# Local imports
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from route_manager import (
    VEHICLES, get_settings, update_settings, 
    estimate_route, save_route, load_data
)

# US States and Major Cities for dropdowns
US_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

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

def main():
    try:
        st.set_page_config(
            page_title="🚛 Route Planner",
            page_icon="🚛",
            layout="wide"
        )
    except:
        pass

    st.title("🚛 Route Planner")
    st.caption("Optimize routes, calculate fuel costs & HOS for your fleet")

    # Sidebar - Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        settings = get_settings()
        
        current_fuel = st.number_input("Diesel Price ($/gal)", value=settings.get('fuel_price', 4.15), step=0.01)
        
        vehs = list(VEHICLES.keys())
        default_veh = st.selectbox("Default Vehicle", vehs, index=vehs.index(settings.get('default_vehicle', 'semi_80k')))
        
        if st.button("Save Settings"):
            update_settings(current_fuel, default_veh)
            st.success("Saved!")

    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Plan Route", "💾 Saved Routes", "ℹ️ Vehicle Profiles"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Trip Details")
            
            # Origin with dropdowns
            st.markdown("**Origin**")
            o_col1, o_col2 = st.columns([2, 1])
            origin_city = o_col1.selectbox("City", MAJOR_CITIES, index=MAJOR_CITIES.index("Chicago"), key="origin_city")
            origin_state = o_col2.selectbox("State", US_STATES, index=US_STATES.index("IL"), key="origin_state")
            origin = f"{origin_city}, {origin_state}"
            
            # Destination with dropdowns
            st.markdown("**Destination**")
            d_col1, d_col2 = st.columns([2, 1])
            dest_city = d_col1.selectbox("City", MAJOR_CITIES, index=MAJOR_CITIES.index("Miami"), key="dest_city")
            dest_state = d_col2.selectbox("State", US_STATES, index=US_STATES.index("FL"), key="dest_state")
            destination = f"{dest_city}, {dest_state}"
            
            # Vehicle Selector
            selected_veh_key = st.selectbox(
                "Vehicle Type", 
                list(VEHICLES.keys()), 
                format_func=lambda x: VEHICLES[x]['name'],
                index=list(VEHICLES.keys()).index(settings.get('default_vehicle', 'semi_80k'))
            )
            selected_veh = VEHICLES[selected_veh_key]
            
            # Custom MPG Override
            default_mpg = selected_veh['avg_mpg']
            custom_mpg = st.number_input("MPG (adjust for your vehicle)", min_value=1.0, max_value=50.0, value=default_mpg, step=0.5, key="custom_mpg")
            
            st.info(f"**Specs:** {custom_mpg} MPG | {selected_veh['gvw']} GVW")
            if selected_veh['hos_rules']:
                st.warning("⏱️ HOS Rules Apply (11/14 rule)")
            
            if st.button("🚀 Calculate Route", type="primary"):
                # Geocoding and Routing (OSRM Public API)
                try:
                    with st.spinner("Optimizing route..."):
                        # 1. Geocode Origin
                        url_base = "https://nominatim.openstreetmap.org/search"
                        headers = {'User-Agent': 'AntigravityAgent/1.0'}
                        r_o = requests.get(f"{url_base}?q={urllib.parse.quote(origin)}&format=json&limit=1", headers=headers)
                        r_d = requests.get(f"{url_base}?q={urllib.parse.quote(destination)}&format=json&limit=1", headers=headers)
                        
                        if not r_o.json() or not r_d.json():
                            st.error("Could not find origin or destination!")
                        else:
                            o_lat, o_lon = r_o.json()[0]['lat'], r_o.json()[0]['lon']
                            d_lat, d_lon = r_d.json()[0]['lat'], r_d.json()[0]['lon']
                            
                            # 2. Get Route (OSRM)
                            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{o_lon},{o_lat};{d_lon},{d_lat}?overview=full"
                            r_route = requests.get(osrm_url)
                            route_data = r_route.json()
                            
                            if route_data['code'] != 'Ok':
                                st.error("Routing failed.")
                            else:
                                # 3. Process Data
                                dist_meters = route_data['routes'][0]['distance']
                                dist_miles = dist_meters * 0.000621371
                                
                                # Estimate Costs (use custom MPG if set)
                                estimates = estimate_route(dist_miles, selected_veh_key, current_fuel, custom_mpg)
                                
                                st.session_state['last_route'] = {
                                    "geometry": route_data['routes'][0]['geometry'],
                                    "origin": [float(o_lat), float(o_lon)],
                                    "dest": [float(d_lat), float(d_lon)],
                                    "estimates": estimates,
                                    "names": (origin, destination)
                                }
                except Exception as e:
                    st.error(f"Error connecting to routing service: {e}")
                    st.caption("Using simplified calculation fallback...")
                    # Fallback logic could go here
        
        with col2:
            if 'last_route' in st.session_state:
                res = st.session_state['last_route']
                est = res['estimates']
                
                # Map
                m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
                
                # Draw Route
                points = polyline.decode(res['geometry'])
                folium.PolyLine(points, color="blue", weight=5, opacity=0.7).add_to(m)
                
                # Markers
                folium.Marker(res['origin'], tooltip="Origin", icon=folium.Icon(color="green", icon="play")).add_to(m)
                folium.Marker(res['dest'], tooltip="Destination", icon=folium.Icon(color="red", icon="stop")).add_to(m)
                
                st_folium(m, width=800, height=500)
                
                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Distance", f"{est['distance']:,.1f} mi")
                m2.metric("Fuel Cost", f"${est['fuel_cost']:,.2f}")
                m3.metric("Est. Time", f"{est['drive_time_hours']} hrs")
                m4.metric("Gallons", f"{est['gallons']} gal")
                
                # HOS Analysis
                if est['hos_info']:
                    hos = est['hos_info']
                    st.subheader("⏱️ Hours of Service Analysis")
                    if hos['is_violation']:
                        st.error(f"⚠️ **VIOLATION:** Trip exceeds 11-hour driving rule.")
                        st.write(f"🛑 **Mandatory 10hr Breaks Needed:** {hos['breaks_needed']}")
                        st.metric("Total Trip Time (with breaks)", f"{hos['total_time_hours']} hrs")
                    else:
                        st.success("✅ Legal trip within single shift.")
                
                # Save Button
                if st.button("💾 Save to History"):
                    save_route(res['names'][0], res['names'][1], est)
                    st.success("Route saved!")

    with tab2:
        st.subheader("saved Routes")
        data = load_data()
        routes = data.get("saved_routes", [])
        
        if not routes:
            st.info("No saved routes yet.")
        else:
            for r in reversed(routes):
                with st.expander(f"🚛 {r['origin']} ➡️ {r['destination']} ({r['timestamp'][:10]})"):
                    d = r['details']
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**Vehicle:** {d['vehicle']}")
                    c1.write(f"**Distance:** {d['distance']:,.1f} mi")
                    c2.write(f"**Fuel Cost:** ${d['fuel_cost']:,.2f}")
                    c2.write(f"**Drive Time:** {d['drive_time_hours']} hrs")
                    if d.get('hos_info'):
                        c3.write(f"**Breaks:** {d['hos_info']['breaks_needed']}")
                        c3.write(f"**Total Time:** {d['hos_info']['total_time_hours']} hrs")

    with tab3:
        st.subheader("ℹ️ Vehicle Profiles")
        for key, veh in VEHICLES.items():
            with st.expander(f"{veh['name']} ({veh['gvw']})"):
                st.write(f"**Avg MPG:** {veh['avg_mpg']}")
                st.write(f"**Speed Factor:** {int(veh['speed_factor']*100)}%")
                st.write(f"**HOS Rules:** {'✅ Yes' if veh['hos_rules'] else '❌ No'}")

if __name__ == "__main__":
    main()
