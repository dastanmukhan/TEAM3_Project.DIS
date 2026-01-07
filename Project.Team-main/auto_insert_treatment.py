import psycopg2
import random
import time
from faker import Faker  # For generating fake medical phrases (install: pip install faker)

# Database connection parameters (replace with yours)
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'hospital_db'
DB_USER = 'postgres'  # Your username
DB_PASSWORD = '123456789'  # Your password
client_encoding='UTF8'

# Initialize Faker
fake = Faker()

# Lists for random values (from dataset)
treatment_types = ['Chemotherapy', 'MRI', 'ECG', 'Physiotherapy', 'X-Ray']
descriptions_base = [  # 20+ unique meaningful phrases (expandable)
    "Basic screening",
    "Standard procedure",
    "Advanced protocol",
    "Initial assessment",
    "Follow-up consultation",
    "Emergency intervention",
    "Routine checkup",
    "Diagnostic imaging",
    "Therapeutic session",
    "Post-operative care",
    "Blood tests and analysis",
    "Minor surgical procedure",
    "Rehabilitation exercises",
    "Pain management plan",
    "Vaccination administration",
    "Allergy testing",
    "Ultrasound examination",
    "Cardiac monitoring",
    "Dermatological treatment",
    "Oncology follow-up",
    "Pediatric evaluation",
    "Endoscopy procedure",
    "Biopsy sampling",
    "Physiotherapy session",
    "Radiotherapy dose"
]

# Connect
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    client_encoding='UTF8'
)
cur = conn.cursor()

# Fetch existing appointment_ids (to respect FK)
cur.execute("SELECT appointment_id FROM appointments ORDER BY appointment_id")
appointments = [row[0] for row in cur.fetchall()]

# Get next treatment_id (after T200)
cur.execute("SELECT COALESCE(MAX(CAST(SUBSTRING(treatment_id FROM 2) AS INTEGER)), 200) FROM treatments")
next_num = cur.fetchone()[0] + 1

print("Script started. Inserting new treatments with varied descriptions every 10 seconds. Stop with Ctrl+C.")

try:
    while True:
        next_id = f"T{next_num:03d}"
        appointment = random.choice(appointments)  # Link to existing appointment
        treatment_type = random.choice(treatment_types)
        # Random description from list (varied, meaningful)
        description = random.choice(descriptions_base)
        # Random cost (100–5000, float)
        cost = round(random.uniform(100.0, 5000.0), 2)
        # Date: Same as appointment or random future
        treatment_date = fake.date_between(start_date='-1y', end_date='+1y').strftime('%Y-%m-%d')
        
        # Insert
        insert_query = """
        INSERT INTO treatments (treatment_id, appointment_id, treatment_type, description, cost, treatment_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (next_id, appointment, treatment_type, description, cost, treatment_date))
        conn.commit()
        
        print(f"Inserted: {next_id} ({treatment_type}, '{description}', Cost: ${cost}, Date: {treatment_date})")
        
        next_num += 1
        time.sleep(2)  # Interval: 10 seconds
        
except KeyboardInterrupt:
    print("Script stopped.")
finally:
    cur.close()
    conn.close()