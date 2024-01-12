import psycopg2

def get_students_hours(students:list, schedules:list) -> list:
    students_str = str(students)[1:-1]
    schedules_str = str(schedules)[1:-1]

    connection = psycopg2.connect(
        host="postgres",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()

    cursor.execute(f"""SELECT student_id, COUNT(CASE WHEN attended THEN 1 END)*2 AS was, COUNT(*)*2 AS need
        FROM attendances
        WHERE student_id IN ({students_str}) AND schedule_id IN ({schedules_str})
        GROUP BY student_id""")
    
    result = cursor.fetchall()
    connection.close()
    return result