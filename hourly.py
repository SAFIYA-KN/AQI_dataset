import requests
import csv
import os
from datetime import datetime

# Read API key from environment variable
API_KEY = os.environ.get("DATA_GOV_API_KEY")

URL = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=579b464db66ec23bdd000001fc3f393d3117471359d8f9458a795e37&format=csv"

URL = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
PARAMS = {
    "api-key": API_KEY,
    "format": "json",
    "limit": 100
}

# Create folder to store daily files
DATA_DIR = "daily_data"
os.makedirs(DATA_DIR, exist_ok=True)

# File name based on current date
today_date = datetime.now().strftime("%Y-%m-%d")
CSV_FILE = f"{DATA_DIR}/aqi_{today_date}.csv"

# Fetch AQI data
response = requests.get(URL, params=PARAMS)
data = response.json()
# CSV headers
headers = [
    "download_date",
    "country",
    "state",
    "city",
    "station",
    "last_update",
    "latitude",
    "longitude",
    "pollutant_id",
    "pollutant_min",
    "pollutant_max",
    "pollutant_avg"
]

#Write to CSV
write_headers = not os.path.exists(CSV_FILE)
with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if write_headers:
        writer.writerow(headers)

    for r in data.get("records", []):
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        r.get("country"),
        r.get("state"),
        r.get("city"),
        r.get("station"),
        r.get("last_update"),
        r.get("latitude"),
        r.get("longitude"),
        r.get("pollutant_id"),
        r.get("min_value"),
        r.get("max_value"),
        r.get("avg_value")
    ])
print(f"Daily AQI dataset saved as {CSV_FILE}")
os.system("git add daily_data/*.csv")
os.system(f'git commit -m "AQI update {datetime.now()}"')
os.system("git push origin main")
