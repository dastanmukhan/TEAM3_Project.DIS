import psycopg2
import random

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'hospital_db'
DB_USER = 'postgres'
DB_PASSWORD = '123456789'

MIN_LAT, MAX_LAT = 47.5, 47.7
MIN_LON, MAX_LON = -122.4, -122.2

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    client_encoding='UTF8'
)
cur = conn.cursor()

cur.execute("""
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS latitude NUMERIC(9,6);
    ALTER TABLE patients ADD COLUMN IF NOT EXISTS longitude NUMERIC(10,6);
""")
conn.commit()

cur.execute("SELECT patient_id FROM patients ORDER BY patient_id")
patients = [row[0] for row in cur.fetchall()]

print(f"Updating coordinates for {len(patients)} patients...")

updated_count = 0
for patient in patients:
    lat = round(random.uniform(MIN_LAT, MAX_LAT), 6)
    lon = round(random.uniform(MIN_LON, MAX_LON), 6)
    
    cur.execute("""
        UPDATE patients 
        SET latitude = %s, longitude = %s 
        WHERE patient_id = %s
    """, (lat, lon, patient))
    
    if cur.rowcount > 0:
        updated_count += 1
        print(f"Updated {patient}: lat={lat}, lon={lon}")

conn.commit()
print(f"Updated {updated_count} records. Refresh in Superset Datasets > patients.")

cur.close()
conn.close()