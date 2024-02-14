import random
import psycopg2

def insert_attendances():
    file = open("SQL/data/sql/attendances.sql", "a")
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()

    cursor.execute(f'SELECT students.id, schedule.id FROM schedule JOIN groups ON groups.id = schedule.group_id JOIN students on groups.id = students.group_id;')
    infos = cursor.fetchall()
    for info in infos:
        attended = random.choice([True, False])
        query = f"CALL insert_attendances({info[0]}, {info[1]}, {attended});"
        cursor.execute(query)
        file.write(query + '\n')

    connection.commit()
    connection.close()
    file.close()

    print('Postgres | Таблица attendances заполнена')