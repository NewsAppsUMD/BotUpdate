import sqlite3

def init_db():
    conn = sqlite3.connect("pg_county_crime.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crimes (
        incident_case_id TEXT PRIMARY KEY,
        date TEXT,
        type TEXT,
        address TEXT,
        sector TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_crime_if_new(crime):
    conn = sqlite3.connect("pg_county_crime.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO crimes (incident_case_id, date, type, address, sector)
            VALUES (?, ?, ?, ?, ?)
        """, (
            crime.get("incident_case_id"),
            crime.get("date"),
            crime.get("clearance_code_inc_type"),
            crime.get("street_address"),
            crime.get("pgpd_sector")
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
