import sqlite3
from datetime import datetime
from collections import Counter

# Connect to the database
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# Fetch and display all rows from the weather_data table
def show_weather_data():
    cursor.execute("SELECT * FROM weather_data")
    rows = cursor.fetchall()
    print("Weather Data:")
    for row in rows:
        print(row)  # Each row is a tuple representing one record

# Fetch and display daily summaries
def show_daily_summaries():
    cursor.execute("SELECT * FROM daily_weather_summary")
    rows = cursor.fetchall()
    print("\nDaily Weather Summaries:")
    for row in rows:
        print(row)

def calculate_daily_summary(cities, date):
    for city in cities:
        print(f"Calculating daily summary for {city} on {date}")
        cursor.execute("""
            SELECT temp, main FROM weather_data WHERE city = ? AND DATE(timestamp) = ?
    """, (city, date))
    
        rows = cursor.fetchall()
        print(f"Fetched rows: {rows}")  # Debugging line to check fetched data

        if rows:
            temps = [row[0] for row in rows]  # Extract temperatures
            conditions = [row[1] for row in rows]  # Extract weather conditions

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
        print(f"Summary stored for {city} on {date}")
    else:
        print(f"No data available for {city} on {date}")

cities_to_process = ["Delhi", "Bangalore", "Mumbai", "Chennai", "Kolkata", "Hyderabad"]

# Display weather data and summaries
show_weather_data()
calculate_daily_summary(cities_to_process, "2024-10-18")  # Adjust date and city as necessary
cursor.execute("SELECT * FROM daily_weather_summary")
rows = cursor.fetchall()
print("Daily Weather Summaries:")
for row in rows:
    print(row)
show_daily_summaries()

# Close the database connection when done
conn.close()
