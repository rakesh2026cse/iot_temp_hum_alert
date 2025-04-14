import Adafruit_DHT
import sqlite3
import time
from datetime import datetime

SENSOR = Adafruit_DHT.DHT11
PIN = 4 

DB_NAME = "database.db"
TEMP_THRESHOLD = 30 

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

def read_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    return temperature, humidity

def insert_data(temp, hum):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)", 
              (temp, hum, timestamp))


    if temp > TEMP_THRESHOLD:
        alert = f" High temperature alert: {temp:.1f}°C at {timestamp}"
        c.execute("INSERT INTO alerts (message, timestamp) VALUES (?, ?)", (alert, timestamp))

    conn.commit()
    conn.close()

def run():
    init_db()
    while True:
        temp, hum = read_sensor()
        if temp is not None and hum is not None:
            insert_data(temp, hum)
            print(f"Logged -> Temp: {temp:.1f}°C, Humidity: {hum:.1f}%")
        else:
            print("Sensor reading failed.")
        time.sleep(10) 

if __name__ == "__main__":
    run()
