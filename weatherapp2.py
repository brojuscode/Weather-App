import requests
import time
import sqlite3
from datetime import datetime
from collections import Counter

# Configurations
API_KEY = "caa12b557b79c93ea5c304097555c8ad"
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
INTERVAL = 10  # Fetch every 5 minutes

# Database setup
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# Ensure tables are created
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        main TEXT,
        temp FLOAT,
        feels_like FLOAT,
        timestamp TIMESTAMP
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_weather_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date DATE,
        avg_temp FLOAT,
        max_temp FLOAT,
        min_temp FLOAT,
        dominant_condition TEXT
    )
""")
conn.commit()

# Fetching data function
def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city,
            "main": data["weather"][0]["main"],
            "temp": data["main"]["temp"] - 273.15,  # Convert to Celsius
            "feels_like": data["main"]["feels_like"] - 273.15,  # Convert to Celsius
            "timestamp": datetime.fromtimestamp(data["dt"]),
        }
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# Store data function
def store_weather_data(data):
    cursor.execute("""
        INSERT INTO weather_data (city, main, temp, feels_like, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (data["city"], data["main"], data["temp"], data["feels_like"], data["timestamp"]))
    conn.commit()
    print(f"Data stored for {data['city']} at {data['timestamp']}")

# Daily summary function
def calculate_daily_summary(city, date):
    print(f"Calculating daily summary for {city} on {date}")
    cursor.execute("""
        SELECT temp, main FROM weather_data
        WHERE city = ? AND DATE(timestamp) = ?
    """, (city, date))

    rows = cursor.fetchall()
    print(f"Fetched rows: {rows}")
    if rows:
        temps = [row[0] for row in rows]
        conditions = [row[1] for row in rows]

        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        dominant_condition = Counter(conditions).most_common(1)[0][0]

        print(f"Inserting summary: Avg: {avg_temp}, Max: {max_temp}, Min: {min_temp}, Dominant: {dominant_condition}")
        cursor.execute("""
            INSERT INTO daily_weather_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (city, date, avg_temp, max_temp, min_temp, dominant_condition))
        conn.commit()
        print(f"Daily summary stored for {city} on {date}")
    else:
        print(f"No data for {city} on {date}")

# Main function
def main():
    while True:
        for city in CITIES:
            data = fetch_weather_data(city)
            if data:
                store_weather_data(data)
        print("Sleeping until next data fetch...")
        time.sleep(INTERVAL)  # Wait for the configured interval

if __name__ == "__main__":
    main()
