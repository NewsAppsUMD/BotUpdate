from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/monthly_crime")
def monthly_crime():
    df = pd.read_csv("monthly_crime.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/crime_type_dist")
def crime_type_dist():
    df = pd.read_csv("crime_type_dist.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/sector_crime")
def sector_crime():
    df = pd.read_csv("sector_crime.csv")
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
