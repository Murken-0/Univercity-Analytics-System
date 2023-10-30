import random
import psycopg2

file = open("group_course.sql", "w")
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
)
cursor = connection.cursor()

query = 'INSERT INTO group_course(course_id, group_id, special) VALUES\n'
for spec in range(1, 5):
    cursor.execute(f'SELECT id FROM groups WHERE speciality_id = {spec}')
    groups_ids = cursor.fetchall()
    for group in groups_ids:        
        course_numbers = [random.randint(1, 48) for _ in range(random.randint(6, 13))]
        special = random.choice([True, False])
        for course in course_numbers:
            query += f"({course}, {group[0]}, {special}),\n"

connection.close()
file.write(query)
file.close()