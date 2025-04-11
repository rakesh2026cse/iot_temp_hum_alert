import Adafruit_DHT
import sqlite3
import time
from datetime import datetime

# Sensor type and GPIO pin
SENSOR = Adafruit_DHT.DHT11
PIN = 4  # GPIO pin used for data signal

DB_NAME = "database.db"
TEMP_THRESHOLD = 30  # Threshold for alert

# Create database tables if they don't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Read data from the sensor
def read_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    return temperature, humidity

# Insert sensor data into database and check for alerts
def insert_data(temp, hum):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert data into sensor_data table
    c.execute("INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)", 
              (temp, hum, timestamp))

    # Check and insert alert if needed
    if temp > TEMP_THRESHOLD:
        alert = f"🔥 High temperature alert: {temp:.1f}°C at {timestamp}"
        c.execute("INSERT INTO alerts (message, timestamp) VALUES (?, ?)", (alert, timestamp))

    conn.commit()
    conn.close()

# Main loop
def run():
    init_db()
    while True:
        temp, hum = read_sensor()
        if temp is not None and hum is not None:
            insert_data(temp, hum)
            print(f"Logged -> Temp: {temp:.1f}°C, Humidity: {hum:.1f}%")
        else:
            print("Sensor reading failed.")
        time.sleep(10)  # Wait 10 seconds before next reading

if __name__ == "__main__":
    run()
