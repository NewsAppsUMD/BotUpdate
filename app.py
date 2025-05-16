from flask import Flask, render_template, jsonify
import pandas as pd
from datetime import datetime  # <-- This was also missing

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/violent_trends')
def violent_trends():
    df = pd.read_csv('Crime_Incidents_July_2023_to_Present_20250516.csv', parse_dates=['Date'])
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df['year_month'] = df['date'].dt.to_period('M').astype(str)

    violent_crimes = [
        "HOMICIDE", "ROBBERY", "RAPE", "AGG. ASSAULT", "ASSAULT",
        "SHOOTING", "MURDER", "CARJACKING", "ARSON", "KIDNAPPING"
    ]

    violent_df = df[df['clearance_code_inc_type'].str.upper().isin(violent_crimes)]
    result = violent_df.groupby('year_month').size().reset_index(name='violent_crime_count')
    return jsonify(result.to_dict(orient='records'))

# ✅ Add route here
@app.route('/api/top_crimes')
def top_crimes():
    df = pd.read_csv('Crime_Incidents_July_2023_to_Present_20250516.csv', parse_dates=['Date'])
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["crime_type"] = df["clearance_code_inc_type"].str.upper()

    violent_crimes = [
        "HOMICIDE", "ROBBERY", "RAPE", "AGG. ASSAULT", "ASSAULT",
        "SHOOTING", "MURDER", "CARJACKING", "ARSON", "KIDNAPPING"
    ]
    violent_df = df[df["crime_type"].isin(violent_crimes)]

    current_year = datetime.now().year
    current_month = datetime.now().month

    this_month_df = violent_df[(violent_df["year"] == current_year) & (violent_df["month"] == current_month)]
    top_violent_this_month = this_month_df["crime_type"].value_counts().head(5).reset_index()
    top_violent_this_month.columns = ["crime_type", "count"]

    this_year_df = df[df["year"] == current_year]
    top_all_this_year = this_year_df["crime_type"].value_counts().head(5).reset_index()
    top_all_this_year.columns = ["crime_type", "count"]

    return jsonify({
        "top_violent_this_month": top_violent_this_month.to_dict(orient='records'),
        "top_all_this_year": top_all_this_year.to_dict(orient='records')
    })



if __name__ == '__main__':
    app.run(debug=True)
