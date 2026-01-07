# TEAM3_Project.DIS
---

# 🏥 Dystopia — Healthcare Analytics Platform

**Dystopia** is a healthcare analytics company focused on turning complex hospital data into clear, actionable insights.
Our mission is to help hospitals and clinics **improve patient care, optimize operations, and enhance financial performance** through data-driven decision making.

In a demanding and fast-changing healthcare environment, Dystopia empowers organizations to operate smarter and more efficiently.

---

## 📊 Project Overview

This project delivers end-to-end analytics for hospital management, combining data engineering, analysis, and visualization.

### Key Analytics Modules

* **VIP Patient Analysis**
  Identify high-value patients based on appointment frequency and billing data to support personalized healthcare services.

* **Appointment Trends**
  Analyze monthly appointment patterns for 2023 to improve workforce planning and resource allocation.

* **Doctor Performance Metrics**
  Rank doctors by revenue and appointment volume to highlight top performers and support training strategies.

* **Payment Method Insights**
  Evaluate revenue distribution across payment methods to streamline billing and financial workflows.

* **Patient Retention Analysis**
  Measure repeat visits to assess loyalty and improve long-term patient engagement.

These insights help hospitals deliver better care while maintaining operational excellence and financial sustainability.

---

## 📸 
<img width="994" height="523" alt="image" src="https://github.com/user-attachments/assets/dcfa46f9-ce8b-4fa6-ba6b-9e77f2f1ee3a" />


**Analytics Dashboard Examples**

* Dashboard Overview
* Appointment Trends Visualization
* Doctor Performance Analysis

<img width="1524" height="678" alt="image" src="https://github.com/user-attachments/assets/16d9abc1-367c-4db1-acd2-c74d81102a4b" />
<img width="1027" height="711" alt="image" src="https://github.com/user-attachments/assets/26d65694-b6eb-4be2-bdaf-40891fe4a24a" />
<img width="1416" height="533" alt="image" src="https://github.com/user-attachments/assets/e4e2351a-677d-4fe7-b0a7-04a16864aae2" />




## 🚀 How to Run the Project

### Requirements

* **PostgreSQL** (port `5432`)
* **Python 3.12**

  * pandas
  * sqlalchemy
  * psycopg2-binary
* **Hospital Management Dataset (CSV)**
  Source:
  [https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset](https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset)

---

### Setup Steps

Clone the repository:

```bash
https://github.com/dastanmukhan/TEAM3_Project.DIS
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Load data into PostgreSQL:

```bash
python load_to_postgres.py
```

Run analytics queries:

```bash
python main.py
```

---

## 🗂 Project Structure

```
├── charts/
│   ├── bar_top_doctors_revenue.png
│   ├── barh_avg_treatment_cost.png
│   ├── hist_bill_amounts.png
│   ├── line_monthly_appointments.png
│   ├── pie_payment_methods.png
│   ├── scatter_patient_engagement.png
├── data/
│   ├── patients.csv
│   ├── doctors.csv
│   ├── appointments.csv
│   ├── billing.csv
│   └── treatments.csv
├── images/
│   ├── placeholder.png
│   └── er_diagram.png
├── exports/
│   └── billing_report.xlsx
├── load_to_postgres.py
├── main.py
├── interactive_graph.py
├── graph.py
├── queries.sql
├── visual_query.sql
├── requirements.txt
└── README.md
```

---

## 🛠 Tools & Technologies

* **Database:** PostgreSQL
* **Programming Language:** Python 3.12

  * pandas
  * sqlalchemy
  * psycopg2-binary
* **Visualization:** Apache Superset (optional)
* **Data Source:** Kaggle — Hospital Management Dataset
* **Version Control:** Git & GitHub

---

## 🧩 ER Diagram

The ER diagram represents the hospital data model, covering relationships between patients, doctors, appointments, treatments, and billing records.

*(Insert ER diagram image from `/images/er_diagram.png`)*

---

## ✨ Why Dystopia?

* Data-driven healthcare decisions
* Clear business and clinical insights
* Scalable analytics architecture
* Ready for real-world hospital environments

---




