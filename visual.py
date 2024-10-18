import sqlite3
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database
conn = sqlite3.connect("weather.db")

# Step 2: Define the plotting function
def plot_multiple_cities_summary(conn, cities):
    cursor = conn.cursor()

    city_data = {}
    for city in cities:
    # Fetch average temperature data for the specified city
        cursor.execute("""
            SELECT date, avg_temp FROM daily_weather_summary WHERE city = ?
        """, (city,))
    
        rows = cursor.fetchall()
    
        if not rows:
            print(f"No data available for {city}.")
            continue  # Skip to the next city if there's no data

    # Unpack the data
        dates, avg_temps = zip(*rows)
        city_data[city] = (dates, avg_temps)

    # Plotting the data
    plt.figure(figsize=(10, 5))  # Optional: Set the size of the figure
    for city, (dates, avg_temps) in city_data.items():
        plt.plot(dates, avg_temps, marker='o', label=f'Avg Temp in {city}')
    plt.title(f"Average Temperature for Multiple Cities")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)  # Rotate date labels for better readability
    plt.legend()
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

# Step 3: Call the function with the desired city
cities_to_plot = ["Delhi", "Bangalore", "Mumbai", "Chennai", "Kolkata", "Hyderabad"]
plot_multiple_cities_summary(conn, cities_to_plot)  # Replace "Delhi" with the desired city

# Step 4: Close the database connection when done
conn.close()
