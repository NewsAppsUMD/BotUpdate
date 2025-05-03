import pandas as pd
import sqlite3

# Load the CSV file
csv_path = "Crime_Incidents_July_2023_to_Present_20250503.csv"
crime_df = pd.read_csv(csv_path)

# Create (or connect to) SQLite database
db_path = "pg_county_crime.db"
conn = sqlite3.connect(db_path)

# Write DataFrame to a SQL table
crime_df.to_sql("crimes", conn, if_exists="replace", index=False)

# Optional: Preview first few rows
preview = pd.read_sql_query("SELECT * FROM crimes LIMIT 5;", conn)
print(preview)

# Optional: Show table structure
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(crimes)")
for col in cursor.fetchall():
    print(col)

# Close connection (optional if you're reusing it)
conn.close()
