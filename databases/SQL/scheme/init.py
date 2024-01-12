import psycopg2

def init_posgres():
    query = ''
    with open("postgres/scheme/init.sql") as file:
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
    print('Postgres | Схема создана')