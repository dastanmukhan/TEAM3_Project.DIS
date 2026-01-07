-- name: pie_payment_methods
-- type: pie
-- title: Distribution of Total Revenue by Payment Method for Paid Bills in 2023
-- xlabel: 
-- ylabel: Total Revenue
SELECT b.payment_method, SUM(b.amount) as total_revenue 
FROM billing b 
JOIN treatments t ON b.treatment_id = t.treatment_id 
JOIN appointments a ON t.appointment_id = a.appointment_id 
WHERE b.payment_status = 'Paid' AND b.bill_date LIKE '2023%%' AND a.appointment_date LIKE '2023%%' 
GROUP BY b.payment_method 
ORDER BY total_revenue DESC;

-- name: bar_top_doctors_revenue
-- type: bar
-- title: Top 10 Doctors by Total Revenue in 2023
-- xlabel: Doctor
-- ylabel: Total Revenue
SELECT d.first_name || ' ' || d.last_name as doctor_name, COALESCE(SUM(b.amount), 0) as total_revenue 
FROM doctors d 
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id 
LEFT JOIN treatments t ON a.appointment_id = t.appointment_id 
LEFT JOIN billing b ON t.treatment_id = b.treatment_id 
WHERE a.appointment_date LIKE '2023%%' OR a.appointment_date IS NULL 
GROUP BY d.doctor_id, d.first_name, d.last_name 
ORDER BY total_revenue DESC 
LIMIT 10;

-- name: barh_avg_treatment_cost
-- type: barh
-- title: Average Treatment Cost by Type in 2023 
-- xlabel: Average Cost
-- ylabel: Treatment Type
SELECT t.treatment_type, AVG(b.amount) as avg_cost 
FROM treatments t 
JOIN billing b ON t.treatment_id = b.treatment_id 
JOIN appointments a ON t.appointment_id = a.appointment_id 
WHERE b.bill_date LIKE '2023%%' AND a.appointment_date LIKE '2023%%' 
GROUP BY t.treatment_type 
ORDER BY avg_cost DESC 
LIMIT 5;

-- name: line_monthly_appointments
-- type: line
-- title: Monthly Appointment Counts in 2023
-- xlabel: Month
-- ylabel: Appointment Count
SELECT SUBSTRING(a.appointment_date FROM 6 FOR 2) as month, COUNT(a.appointment_id) as count 
FROM appointments a 
JOIN doctors d ON a.doctor_id = d.doctor_id 
JOIN patients p ON a.patient_id = p.patient_id 
WHERE a.appointment_date LIKE '2023%%' 
GROUP BY month 
ORDER BY month;

-- name: hist_bill_amounts
-- type: hist
-- title: Distribution of Bill Amounts in 2023
-- xlabel: Amount
-- ylabel: Frequency
SELECT b.amount 
FROM billing b 
JOIN treatments t ON b.treatment_id = t.treatment_id 
JOIN appointments a ON t.appointment_id = a.appointment_id 
WHERE b.bill_date LIKE '2023%%' AND a.appointment_date LIKE '2023%%';

-- name: scatter_patient_engagement
-- type: scatter
-- title: Patient Appointment Count vs Total Billed in 2023
-- xlabel: Appointment Count
-- ylabel: Total Billed
SELECT COUNT(a.appointment_id) as appointment_count, COALESCE(SUM(b.amount), 0) as total_billed 
FROM patients p 
LEFT JOIN appointments a ON p.patient_id = a.patient_id 
LEFT JOIN treatments t ON a.appointment_id = t.appointment_id 
LEFT JOIN billing b ON t.treatment_id = b.treatment_id 
WHERE a.appointment_date LIKE '2023%%' OR a.appointment_date IS NULL 
GROUP BY p.patient_id;