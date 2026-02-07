import json
import os
import math
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "router.json")

# Vehicle Profiles
VEHICLES = {
    "car": {
        "name": "🚗 Regular Car",
        "description": "Standard Trip",
        "gvw": "N/A",
        "avg_mpg": 25.0,
        "hos_rules": False,
        "speed_factor": 1.0  # Car goes speed limit
    },
    "hotshot_noncdl": {
        "name": "🚚 Hotshot (Non-CDL)",
        "description": "26,000 lbs GVW",
        "gvw": "26k",
        "avg_mpg": 10.0,
        "hos_rules": False, # Usually not subject to full HOS if under 26k commercial used privately or short haul, but simplifying for user request
        "speed_factor": 0.95
    },
    "hotshot_cdl": {
        "name": "🚛 Hotshot (CDL)",
        "description": "36,000 lbs GVW",
        "gvw": "36k",
        "avg_mpg": 8.5,
        "hos_rules": True,
        "speed_factor": 0.90
    },
    "semi_80k": {
        "name": "🚛 Commercial Semi",
        "description": "80,000 lbs GVW",
        "gvw": "80k",
        "avg_mpg": 6.5,
        "hos_rules": True,
        "speed_factor": 0.85 # Truck speed limits often lower
    }
}

def load_data():
    """Load settings and saved routes."""
    if not os.path.exists(DATA_FILE):
        return {"saved_routes": [], "settings": {"fuel_price": 4.15, "default_vehicle": "semi_80k"}}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save settings and routes."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def get_settings():
    return load_data().get("settings", {})

def update_settings(fuel_price, default_vehicle):
    data = load_data()
    data["settings"]["fuel_price"] = fuel_price
    data["settings"]["default_vehicle"] = default_vehicle
    save_data(data)

def calculate_hos(drive_hours):
    """
    Calculate Hours of Service impacts.
    Rule: 11 hours driving max per 14-hour window. 10 hour break required.
    """
    # Simple logic: If drive time > 11 hours, add 10 hours for every 11 hour block
    breaks_needed = math.floor(drive_hours / 11)
    total_trip_time = drive_hours + (breaks_needed * 10)
    
    return {
        "breaks_needed": breaks_needed,
        "total_time_hours": total_trip_time,
        "legal_driving_limit": 11,
        "is_violation": drive_hours > 11
    }

def estimate_route(distance_miles, vehicle_type, fuel_price, custom_mpg=None):
    """
    Estimate route details based on straight math input.
    In a real version, this accepts coordinates/API data.
    """
    profile = VEHICLES.get(vehicle_type, VEHICLES["car"])
    
    # Use custom MPG if provided, otherwise use profile default
    mpg = custom_mpg if custom_mpg else profile["avg_mpg"]
    
    # Calculate costs
    gallons_needed = distance_miles / mpg
    fuel_cost = gallons_needed * fuel_price
    
    # Calculate time (assuming 60mph base avg speed * speed factor)
    avg_speed = 60 * profile["speed_factor"]
    drive_hours = distance_miles / avg_speed
    
    # HOS Logic
    hos_info = None
    if profile["hos_rules"]:
        hos_info = calculate_hos(drive_hours)
        total_time_hours = hos_info["total_time_hours"]
    else:
        total_time_hours = drive_hours
        
    return {
        "distance": distance_miles,
        "vehicle": profile["name"],
        "mpg": profile["avg_mpg"],
        "gallons": round(gallons_needed, 1),
        "fuel_cost": round(fuel_cost, 2),
        "drive_time_hours": round(drive_hours, 1),
        "total_trip_time_hours": round(total_time_hours, 1),
        "hos_info": hos_info
    }

def save_route(origin, destination, details):
    data = load_data()
    route = {
        "id": len(data["saved_routes"]) + 1,
        "origin": origin,
        "destination": destination,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    data["saved_routes"].append(route)
    save_data(data)
