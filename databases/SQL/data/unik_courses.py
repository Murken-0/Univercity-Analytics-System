import psycopg2

def insert_unik_courses():
    query = ''
    with open("SQL/data/sql/unik_courses.sql") as file:
        query = file.read()

    connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
    print('Postgres | Таблицы unversities - courses заполнены')