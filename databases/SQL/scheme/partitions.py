from datetime import datetime, timedelta
import psycopg2

def create_partitions():
    connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
    )
    cursor = connection.cursor()

    year = 2022
    query = ''
    for week_num in range(1, 53):
        start_date = datetime.strptime(f"{year}-W{week_num:02d}-0", "%Y-W%U-%w") + timedelta(days=1)
        end_date = start_date + timedelta(days=7)

        query += f"CREATE TABLE attendances_y{year}_w{week_num} PARTITION OF attendances\n"
        query += f"    FOR VALUES FROM ('{start_date.strftime('%Y-%m-%d')}') TO ('{end_date.strftime('%Y-%m-%d')}');\n"
    
    cursor.execute(query)
    connection.commit()
    connection.close()

    with open('SQL/scheme/partitions.sql', "w") as file:
        file.write(query)
    print('Postgres | Партиции созданы')