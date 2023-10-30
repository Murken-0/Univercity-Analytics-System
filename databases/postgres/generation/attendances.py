import random
import psycopg2

file = open("insert_attendances.sql", "a")
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
)
cursor = connection.cursor()

for student in range(501, 1001):
    cursor.execute(f'SELECT classes.id FROM classes JOIN courses ON classes.course_id = courses.id JOIN student_course ON student_course.course_id = courses.id JOIN students ON student_course.student_id = students.id WHERE students.id = {student}')
    classes_ids = cursor.fetchall()
    for class_id in classes_ids:
        attended = random.choice([True, False])
        query = f"CALL insert_attendances({student}, {class_id[0]}, {attended});"
        cursor.execute(query)
        file.write(query + '\n')

connection.commit()
connection.close()
file.close()