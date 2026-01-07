import psycopg2

conn = psycopg2.connect(
    dbname="hospital_db",
    user="postgres",
    password="123456789",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
with open("queries.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(";") if q.strip()]

for i, query in enumerate(queries, start=1):
    print(f"\n--- Results for Query {i} ---")
    try:
        cursor.execute(query)
        try:
            rows = cursor.fetchall()
            if rows:
                colnames = [desc[0] for desc in cursor.description]
                print(f"Columns: {colnames}")
                for row in rows[:10]:
                    print(row)
            else:
                print("No data returned")
        except psycopg2.ProgrammingError as e:
            print(f"No data to display: {e}")
    except Exception as e:
        print(f"Error executing query {i}: {e}")

cursor.close()
conn.close()