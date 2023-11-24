import psycopg2

def get_schedule_by_classes(class_ids:list) -> list:
    classes = str(class_ids)[1:-1]
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute(f"""SELECT id
                        FROM schedule
                        WHERE class_id IN ({classes})""")
    return cursor.fetchall()


def get_attended_percentage(schedule_ids:list, student_ids:list, start_date:str, end_date:str) -> list:
    schedules = str(schedule_ids)[1:-1]
    students = str(student_ids)[1:-1]
    
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute(f"""SELECT student_id, AVG(CASE WHEN attended THEN 1 ELSE 0 END) * 100 AS attendance_percentage 
                        FROM attendances
                        WHERE schedule_id IN ({schedules}) AND student_id IN ({students}) AND schedule_date BETWEEN '{start_date}' AND '{end_date}'
                        GROUP BY student_id
                        ORDER BY attendance_percentage ASC
                        LIMIT 10""")
    result = cursor.fetchall()
    connection.close()
    return result