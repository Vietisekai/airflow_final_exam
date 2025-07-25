import psycopg2

def check_table_counts():
    conn = psycopg2.connect("host=postgres dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()
    tables = ['songplays', 'users', 'songs', 'artists', 'time']
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        result = cur.fetchone()
        if result[0] == 0:
            raise ValueError(f"Data quality check failed: {table} is empty!")
        else:
            print(f"Table check passed: {table} has {result[0]} records.")
    cur.close()
    conn.close()