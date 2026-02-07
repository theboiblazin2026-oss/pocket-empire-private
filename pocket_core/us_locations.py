# US States and Major Cities for Pocket Empire
# This module provides standardized location data for dropdowns across the app

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
    "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
]

STATE_ABBREVIATIONS = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", 
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", 
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", 
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", 
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", 
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", 
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", 
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", 
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", 
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", 
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", 
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", 
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", 
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# Major trucking hub cities by state (most common for freight)
MAJOR_CITIES = {
    "Georgia": ["Atlanta", "Savannah", "Augusta", "Macon", "Columbus"],
    "Texas": ["Houston", "Dallas", "San Antonio", "Austin", "Fort Worth", "El Paso"],
    "California": ["Los Angeles", "San Francisco", "San Diego", "Oakland", "Fresno"],
    "Florida": ["Miami", "Jacksonville", "Tampa", "Orlando", "Fort Lauderdale"],
    "Illinois": ["Chicago", "Aurora", "Rockford", "Joliet", "Springfield"],
    "Tennessee": ["Memphis", "Nashville", "Knoxville", "Chattanooga"],
    "Ohio": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron"],
    "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown", "Harrisburg"],
    "New York": ["New York City", "Buffalo", "Rochester", "Syracuse", "Albany"],
    "New Jersey": ["Newark", "Jersey City", "Paterson", "Elizabeth"],
    "North Carolina": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem"],
    "Indiana": ["Indianapolis", "Fort Wayne", "Evansville", "South Bend"],
    "Missouri": ["Kansas City", "St. Louis", "Springfield", "Columbia"],
    "Arizona": ["Phoenix", "Tucson", "Mesa", "Chandler"],
    "Nevada": ["Las Vegas", "Reno", "Henderson"],
    "Washington": ["Seattle", "Spokane", "Tacoma"],
    "Colorado": ["Denver", "Colorado Springs", "Aurora"],
    "Virginia": ["Virginia Beach", "Norfolk", "Richmond", "Newport News"],
    "Maryland": ["Baltimore", "Frederick", "Gaithersburg"],
    "Louisiana": ["New Orleans", "Baton Rouge", "Shreveport"],
    "Alabama": ["Birmingham", "Montgomery", "Mobile", "Huntsville"],
    "Kentucky": ["Louisville", "Lexington", "Bowling Green"],
    "South Carolina": ["Charleston", "Columbia", "Greenville"],
    "Mississippi": ["Jackson", "Gulfport", "Southaven"],
    "Arkansas": ["Little Rock", "Fort Smith", "Fayetteville"],
    "Oklahoma": ["Oklahoma City", "Tulsa", "Norman"],
    "Kansas": ["Wichita", "Kansas City", "Topeka"],
    "Utah": ["Salt Lake City", "West Valley City", "Provo"],
    "Oregon": ["Portland", "Salem", "Eugene"],
    "Michigan": ["Detroit", "Grand Rapids", "Lansing", "Ann Arbor"],
    "Minnesota": ["Minneapolis", "St. Paul", "Rochester"],
    "Wisconsin": ["Milwaukee", "Madison", "Green Bay"],
    "Iowa": ["Des Moines", "Cedar Rapids", "Davenport"],
    "Nebraska": ["Omaha", "Lincoln", "Grand Island"],
}

def get_abbreviation(state_name):
    """Get state abbreviation from full name"""
    return STATE_ABBREVIATIONS.get(state_name, "")

def get_cities(state_name):
    """Get major cities for a state"""
    return MAJOR_CITIES.get(state_name, [])

def filter_by_state(address, state_abbrev):
    """Check if an address contains a state abbreviation"""
    if not address or not state_abbrev:
        return True
    return state_abbrev in str(address).upper()
