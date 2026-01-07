import psycopg2
import random
import time
from faker import Faker  

# Database connection parameters (replace with yours)
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'hospital_db'
DB_USER = 'postgres'  # Your username
DB_PASSWORD = '123456789'  # Your password

# Initialize Faker for random data
fake = Faker()

# Lists for random values
specializations = ['Dermatology', 'Pediatrics', 'Oncology']
hospital_branches = ['Central Hospital', 'Eastside Clinic', 'Westside Clinic']

# Connect with explicit UTF-8 encoding
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    client_encoding='UTF8'
)
cur = conn.cursor()

# Get next ID (after D010; adjust if needed)
cur.execute("SELECT COALESCE(MAX(CAST(SUBSTRING(doctor_id FROM 2) AS INTEGER)), 10) FROM doctors")
next_num = cur.fetchone()[0] + 1

print("Script started. Inserting new doctors every 10 seconds. Stop with Ctrl+C.")

try:
    while True:
        next_id = f"D{next_num:03d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        specialization = random.choice(specializations)
        # Generate clean 10-digit phone as integer (bigint-compatible)
        phone_number = int(fake.numerify('##########'))  # Pure digits, e.g., 1234567890
        years_experience = random.randint(1, 30)
        hospital_branch = random.choice(hospital_branches)
        email = fake.email()  # Random email
        
        # Insert
        insert_query = """
        INSERT INTO doctors (doctor_id, first_name, last_name, specialization, phone_number, years_experience, hospital_branch, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (next_id, first_name, last_name, specialization, phone_number, years_experience, hospital_branch, email))
        conn.commit()
        
        print(f"Inserted: {next_id} ({first_name} {last_name}, {specialization}, {years_experience} years, {hospital_branch})")
        
        next_num += 1
        time.sleep(2)  # Interval: 10 seconds (as in Task 2)
        
except KeyboardInterrupt:
    print("Script stopped.")
finally:
    cur.close()
    conn.close()