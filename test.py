import sqlite3

conn = sqlite3.connect("pg_county_crime.db")
cursor = conn.cursor()

cursor.execute("SELECT date FROM crimes LIMIT 5;")
dates = cursor.fetchall()
for row in dates:
    print(row[0])

conn.close()
