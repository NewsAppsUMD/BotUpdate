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

    # Step 1: Identify top 5 most common crime types overall
    top5_types = (
        df.groupby("clearance_code_inc_type")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index.tolist()
    )

    # Step 2: Filter the full dataset to only include those top 5 types
    df_top5 = df[df["clearance_code_inc_type"].isin(top5_types)]

    return jsonify(df_top5.to_dict(orient="records"))


@app.route("/api/sector_crime")
def sector_crime():
    df = pd.read_csv("sector_crime.csv")
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
