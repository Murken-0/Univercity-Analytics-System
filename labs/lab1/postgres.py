import psycopg2

def get_attended_percentage(class_ids:list, start_date:str, end_date:str) -> list:
    classes = str(class_ids)[1:-1]
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute(f"""SELECT students.code, AVG(CASE WHEN attended THEN 1 ELSE 0 END) * 100 AS attendance_percentage 
                        FROM schedule
                        JOIN attendances ON schedule.id = attendances.schedule_id
                        JOIN students ON attendances.student_id = students.id
                        WHERE class_id IN ({classes}) AND date BETWEEN '{start_date}' AND '{end_date}'
                        GROUP BY students.id
                        ORDER BY attendance_percentage ASC
                        LIMIT 10""")
    result = cursor.fetchall()
    connection.close()
    return result