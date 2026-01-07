-- Basic Query 1: Select first 10 rows from appointments table
SELECT * FROM appointments LIMIT 10;

-- Basic Query 2: Filter appointments in 2023 and sort by appointment_id
SELECT appointment_id, patient_id, doctor_id, appointment_date
FROM appointments
WHERE appointment_date LIKE '2023%'
ORDER BY appointment_id;

-- Basic Query 3: Aggregate billing data by payment status
SELECT payment_status, 
       COUNT(*) as bill_count, 
       AVG(amount) as avg_amount, 
       MIN(amount) as min_amount, 
       MAX(amount) as max_amount
FROM billing
GROUP BY payment_status;

-- Basic Query 4: Join patients and appointments to get patient appointment details
SELECT p.patient_id, p.first_name, p.last_name, a.appointment_id, a.appointment_date
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
LIMIT 10;

-- Analytical Query 1: VIP Patients: Top 10 patients by appointment count and total billing
SELECT p.patient_id, p.first_name, p.last_name, COUNT(a.appointment_id) as appointment_count, 
       COALESCE(SUM(b.amount), 0) as total_billed
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
LEFT JOIN billing b ON p.patient_id = b.patient_id
WHERE a.appointment_date LIKE '2023%' OR a.appointment_date IS NULL
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY appointment_count DESC, total_billed DESC
LIMIT 10;

-- Analytical Query 2: Uncovers monthly patterns in 2023 for staffing optimization
SELECT SUBSTRING(appointment_date FROM 6 FOR 2) as month, 
       COUNT(appointment_id) as appointment_count
FROM appointments
WHERE appointment_date LIKE '2023%'
GROUP BY month
ORDER BY month;

-- Analytical Query 3: Highlights doctors driving the most billing revenue
SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, 
       COALESCE(SUM(b.amount), 0) as total_revenue
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
LEFT JOIN treatments t ON a.appointment_id = t.appointment_id
LEFT JOIN billing b ON t.treatment_id = b.treatment_id
WHERE a.appointment_date LIKE '2023%' OR a.appointment_date IS NULL
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY total_revenue DESC
LIMIT 10;

-- Analytical Query 4: Analyzes popular payment methods in 2023
SELECT b.payment_method, 
       SUM(b.amount) as total_revenue, 
       COUNT(b.bill_id) as bill_count, 
       AVG(b.amount) as avg_bill_amount
FROM billing b
WHERE b.payment_status = 'Paid' AND b.bill_date LIKE '2023%'
GROUP BY b.payment_method
ORDER BY total_revenue DESC;

-- Analytical Query 5: Identifies busiest days of the week for appointments in 2023
SELECT TO_CHAR(TO_DATE(a.appointment_date, 'YYYY-MM-DD'), 'Day') as day_of_week, 
       COUNT(a.appointment_id) as appointment_count
FROM appointments a
WHERE a.appointment_date LIKE '2023%'
GROUP BY day_of_week
ORDER BY appointment_count DESC;

-- Analytical Query 6: Calculates average days between appointment and billing for paid bills in 2023
SELECT t.treatment_type, 
       AVG(TO_DATE(b.bill_date, 'YYYY-MM-DD') - TO_DATE(a.appointment_date, 'YYYY-MM-DD')) as avg_billing_lag_days
FROM treatments t
JOIN appointments a ON t.appointment_id = a.appointment_id
JOIN billing b ON t.treatment_id = b.treatment_id
WHERE b.payment_status = 'Paid' AND b.bill_date LIKE '2023%' AND a.appointment_date LIKE '2023%'
GROUP BY t.treatment_type
HAVING COUNT(b.bill_id) >= 1
ORDER BY avg_billing_lag_days DESC
LIMIT 10;

-- Analytical Query 7: Identifies strong doctor-patient relationships in 2023
SELECT d.doctor_id, d.first_name AS doctor_first_name, d.last_name AS doctor_last_name, p.patient_id, p.first_name AS patient_first_name, p.last_name AS patient_last_name, 
       COUNT(a.appointment_id) as appointment_count
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
JOIN patients p ON a.patient_id = a.patient_id
WHERE a.appointment_date LIKE '2023%'
GROUP BY d.doctor_id, d.first_name, d.last_name, p.patient_id, p.first_name, p.last_name
ORDER BY appointment_count DESC
LIMIT 10;

-- Analytical Query 8: Pinpoints doctors with high patient demand in 2023
SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, 
       COUNT(a.appointment_id) as appointment_count
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
WHERE a.appointment_date LIKE '2023%' OR a.appointment_date IS NULL
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY appointment_count DESC
LIMIT 10;

-- Analytical Query 9: Identifies high-cost treatments in 2023
SELECT t.treatment_type, 
       AVG(b.amount) as avg_treatment_cost, 
       COUNT(b.bill_id) as bill_count
FROM treatments t
JOIN billing b ON t.treatment_id = b.treatment_id
WHERE b.bill_date LIKE '2023%'
GROUP BY t.treatment_type
HAVING COUNT(b.bill_id) >= 1
ORDER BY avg_treatment_cost DESC
LIMIT 10;

-- Analytical Query 10: Calculates percentage of patients with multiple appointments in 2023
WITH patient_appointments AS (
    SELECT p.patient_id, 
           COUNT(a.appointment_id) as appointment_count
    FROM patients p
    LEFT JOIN appointments a ON p.patient_id = a.patient_id
    WHERE a.appointment_date LIKE '2023%' OR a.appointment_date IS NULL
    GROUP BY p.patient_id
)
SELECT 
    SUM(CASE WHEN appointment_count > 1 THEN 1 ELSE 0 END) as repeat_patients,
    COUNT(*) as total_patients,
    ROUND(SUM(CASE WHEN appointment_count > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as retention_rate_percent
FROM patient_appointments;