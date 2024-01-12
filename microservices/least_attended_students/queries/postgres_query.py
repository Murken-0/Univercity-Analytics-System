import psycopg2

def get_attended_percentage(students:list, schedules:list, start_date:str, end_date:str) -> list:
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
    cursor.execute(f"""SELECT student_id, AVG(CASE WHEN attended THEN 1 ELSE 0 END) * 100 AS attendance_percentage 
                        FROM attendances
                        WHERE schedule_id IN ({schedules_str}) AND student_id IN ({students_str}) AND schedule_date BETWEEN '{start_date}' AND '{end_date}'
                        GROUP BY student_id
                        ORDER BY attendance_percentage ASC
                        LIMIT 10""")
    result = cursor.fetchall()
    connection.close()
    return result