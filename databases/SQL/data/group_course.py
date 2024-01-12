import random
import psycopg2

def insert_group_course():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM courses")
    courses = [i[0] for i in cursor.fetchall()]

    query = 'INSERT INTO group_course(course_id, group_id, special) VALUES\n'
    for spec in range(1, 5):
        cursor.execute(f'SELECT id FROM groups WHERE speciality_id = {spec}')
        groups_ids = cursor.fetchall()
        for group in groups_ids:        
            course_numbers = [random.choice(courses) for _ in range(random.randint(6, 13))]
            special = random.choice([True, False])
            for course in course_numbers:
                query += f"({course}, {group[0]}, {special}),\n"
    query = query[:-2]

    cursor.execute(query)
    connection.commit()
    connection.close()

    with open("postgres/data/sql/group_course.sql", "w") as file:
        file.write(query+ ';')
    
    print('Postgres | Таблица group_course заполнена')