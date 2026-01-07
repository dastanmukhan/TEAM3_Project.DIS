import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = 'postgres'
DB_PASSWORD = '123456789'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'hospital_db'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

csv_files = {
    'patients': r'D:\User\Documents\visual\data\patients.csv',
    'doctors': r'D:\User\Documents\visual\data\doctors.csv',
    'appointments': r'D:\User\Documents\visual\data\appointments.csv',
    'billing': r'D:\User\Documents\visual\data\billing.csv',
    'treatments': r'D:\User\Documents\visual\data\treatments.csv'
}

# Dictionary to rename columns if they differ in CSV files
column_mappings = {
    'treatments': {'appointmentID': 'appointment_id'},  # Adjust if the column name in treatments.csv is different
    'billing': {'patientID': 'patient_id', 'treatmentID': 'treatment_id'}  # Adjust if column names differ
}

for table_name, file_path in csv_files.items():
    try:
        df = pd.read_csv(file_path)
        print(f"Columns in {table_name}.csv: {list(df.columns)}")
        if table_name in column_mappings:
            df = df.rename(columns=column_mappings[table_name])
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Successfully loaded {file_path} into table '{table_name}'")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

with engine.connect() as connection:
    try:
        connection.execute(text("""
            ALTER TABLE patients ADD PRIMARY KEY (patient_id);
            ALTER TABLE doctors ADD PRIMARY KEY (doctor_id);
            ALTER TABLE appointments ADD PRIMARY KEY (appointment_id);
            ALTER TABLE appointments ADD CONSTRAINT fk_patient 
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id);
            ALTER TABLE appointments ADD CONSTRAINT fk_doctor 
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id);
            ALTER TABLE treatments ADD PRIMARY KEY (treatment_id);
            ALTER TABLE treatments ADD CONSTRAINT fk_appointment 
                FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id);
            ALTER TABLE billing ADD PRIMARY KEY (bill_id);
            ALTER TABLE billing ADD CONSTRAINT fk_patient 
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id);
            ALTER TABLE billing ADD CONSTRAINT fk_treatment 
                FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id);
        """))
        connection.commit()
        print("Successfully applied constraints")
    except Exception as e:
        print(f"Error applying constraints: {e}")