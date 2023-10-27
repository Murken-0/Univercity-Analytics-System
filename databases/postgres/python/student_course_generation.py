import random
import psycopg2

file = open("insert_student_course.sql", "w")
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
)
cursor = connection.cursor()

query = 'INSERT INTO student_course(course_id, student_id) VALUES\n'
for course_id in range(1, 49):
    group_numbers = [random.randint(1, 15) for _ in range(1, random.randint(2, 6))]
    v = str(group_numbers).replace("]", "").replace("[", "")
    cursor.execute(f'SELECT id FROM students WHERE group_id IN ({v})')
    student_ids = cursor.fetchall()
    for student_id in student_ids:
        query += f"({course_id}, {student_id[0]}),\n"

connection.close()
file.write(query + '\n')
file.close()