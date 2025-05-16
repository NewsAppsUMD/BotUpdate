from flask import Flask, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/api/trends")
def get_trends():
    conn = sqlite3.connect("pg_county_crime.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT city, strftime('%Y', date) as year, COUNT(*) as count
        FROM crimes
        GROUP BY city, year
    """)
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for city, year, count in rows:
        if city not in data:
            data[city] = {}
        data[city][year] = count

    return jsonify(data)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
