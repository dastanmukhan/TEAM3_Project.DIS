import psycopg2
from datetime import datetime, timedelta
import random
import time

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'hospital_db'
DB_USER = 'postgres' 
DB_PASSWORD = '123456789' 

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    client_encoding='UTF8'  
)
cur = conn.cursor()

cur.execute("SELECT patient_id FROM patients ORDER BY patient_id")
patients = [row[0] for row in cur.fetchall()]

cur.execute("SELECT doctor_id FROM doctors ORDER BY doctor_id")
doctors = [row[0] for row in cur.fetchall()]

reasons = ['Therapy', 'Consultation', 'Emergency', 'Checkup', 'Follow-up']
statuses = ['Scheduled', 'No-show', 'Cancelled', 'Completed']
times = ['08:00:00', '09:15:00', '10:30:00', '11:45:00', '12:00:00', '13:15:00', '14:30:00', '15:45:00', '16:00:00', '17:15:00']

cur.execute("SELECT COALESCE(MAX(CAST(SUBSTRING(appointment_id FROM 2) AS INTEGER)), 200) FROM appointments")
next_num = cur.fetchone()[0] + 1

print("Script started. Inserting new appointments every 20 seconds.")

try:
    while True:
        next_id = f"A{next_num:03d}"
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        
        base_date = datetime.now()
        days_ahead = random.randint(1, 365)
        app_date = base_date + timedelta(days=days_ahead)
        app_date_str = app_date.strftime('%Y-%m-%d')
        
        app_time = random.choice(times)
        reason = random.choice(reasons)
        status = random.choice(statuses)
        
        insert_query = """
        INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (next_id, patient, doctor, app_date_str, app_time, reason, status))
        conn.commit()
        
        print(f"Inserted: {next_id} for {patient} with {doctor} ({reason}, {status}) on {app_date_str} {app_time}")
        
        next_num += 1
        time.sleep(2)  
        
except KeyboardInterrupt:
    print("Script stopped.")
finally:
    cur.close()
    conn.close()