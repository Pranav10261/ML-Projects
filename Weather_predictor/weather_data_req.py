import requests
import pandas as pd

def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "country": "IN"}
    response = requests.get(url, params=params).json()
    result = response["results"][0]
    return result["latitude"], result["longitude"]

def get_historical_weather(city_name, start_date, end_date):
    lat, lon = get_coordinates(city_name)
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
      "latitude": lat,
      "longitude": lon,
      "start_date": start_date,
      "end_date": end_date,
      "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
      "timezone": "Asia/Kolkata"
    }
    response = requests.get(url, params=params).json()
    
    d = pd.DataFrame(response["daily"])
    return d

# --- Example usage ---
d = get_historical_weather("Kochi", "2015-01-01", "2026-08-07")
print(d.head())
d.to_csv("kochi_10yr_weather.csv", index=False)
print(d.shape)
print(d.tail())
