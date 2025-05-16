import sqlite3

# Sector-to-City mapping
sector_map = {
    "B": "Bowie",
    "G": "Greenbelt",
    "H": "Hyattsville",
    "W": "Oxon Hill",
    "K": "Capitol Heights",
    "M": "College Park"
}

def init_db():
    conn = sqlite3.connect("pg_county_crime.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crimes (
        incident_case_id TEXT PRIMARY KEY,
        date TEXT,
        type TEXT,
        address TEXT,
        sector TEXT,
        city TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_crime_if_new(crime):
    conn = sqlite3.connect("pg_county_crime.db")
    cursor = conn.cursor()

    sector = crime.get("pgpd_sector")
    city = sector_map.get(sector, "Unknown")

    try:
        cursor.execute("""
            INSERT INTO crimes (incident_case_id, date, type, address, sector, city)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            crime.get("incident_case_id"),
            crime.get("date"),
            crime.get("clearance_code_inc_type"),
            crime.get("street_address"),
            sector,
            city
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Duplicate entry
    finally:
        conn.close()

def summarize_violent_crimes(start_date, end_date):
    conn = sqlite3.connect("pg_county_crime.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, COUNT(*) 
        FROM crimes
        WHERE date BETWEEN ? AND ?
        AND (type LIKE '%HOMICIDE%' OR type LIKE '%ASSAULT%' OR type LIKE '%ROBBERY%' 
             OR type LIKE '%SHOOTING%' OR type LIKE '%SEX OFFENSE%')
        GROUP BY type
    """, (start_date, end_date))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_db()
