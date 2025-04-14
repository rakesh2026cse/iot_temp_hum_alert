from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT temperature, humidity, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1")
    latest = c.fetchone()

    c.execute("SELECT message, timestamp FROM alerts ORDER BY id DESC LIMIT 5")
    alerts = c.fetchall()

    conn.close()

    return render_template("index.html", latest=latest, alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)
