import random
from datetime import datetime, timedelta
import psycopg2

def insert_schedule():
    start_date = datetime.strptime("2022-02-07", '%Y-%m-%d')
    end_date = datetime.strptime("2022-06-11", '%Y-%m-%d')
    delta = int((end_date - start_date).days / 16)
    dates = [start_date + timedelta(days=i * delta) for i in range(16)]

    connection = psycopg2.connect(
        host='localhost', 
        port='5432', 
        dbname='practice', 
        user='admin', 
        password='admin'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM courses")
    courses = [i[0] for i in cursor.fetchall()]

    query = f"INSERT INTO schedule (class_id, group_id, date, pair_number) VALUES\n"

    for course_id in courses:
        cursor.execute(f"SELECT id FROM classes WHERE course_id = {course_id}")
        classes = [cl[0] for cl in cursor.fetchall()]
        for i, cl in enumerate(classes):
            cursor.execute(f"SELECT groups.id FROM classes JOIN courses ON classes.course_id = courses.id JOIN group_course ON group_course.course_id = courses.id JOIN groups ON group_course.group_id = groups.id WHERE classes.id = {cl}")
            groups = [gr[0] for gr in cursor.fetchall()]
            for gr in groups:
                pair = random.randint(1,6)
                query += f"({cl}, {gr}, '{dates[i]}', {pair}),\n"
    query = query[:-2]

    cursor.execute(query)
    connection.commit()
    connection.close()

    with open("SQL/data/sql/sheldue.sql", "w") as file:
        file.write(query+ ';')
    
    print('Postgres | Таблица schedule заполнена')