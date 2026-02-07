import requests

def get_weather(lat=33.7490, lon=-84.3880):
    """
    Fetches weather for Atlanta (default) via OpenMeteo (Free, No Key).
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&timezone=auto"
        r = requests.get(url)
        data = r.json()

        current = data.get('current', {})
        daily = data.get('daily', {})

        temp_now = current.get('temperature_2m', 'N/A')
        
        # Weather Codes (WMO)
        code = current.get('weather_code', 0)
        condition = "Clear"
        if 1 <= code <= 3: condition = "Cloudy"
        elif 50 <= code <= 67: condition = "Rainy"
        elif 70 <= code <= 77: condition = "Snowy"
        elif code >= 95: condition = "Thunderstorm"

        high = daily.get('temperature_2m_max', ['N/A'])[0]
        low = daily.get('temperature_2m_min', ['N/A'])[0]

        return {
            "temp_now": temp_now,
            "condition": condition,
            "high": high,
            "low": low,
            "location": "Atlanta, GA"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(get_weather())
