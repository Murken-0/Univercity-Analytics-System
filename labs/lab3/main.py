from neo4j_query import get_courses_schedules, get_students
from postgres_query import get_students_hours
from redis_query import get_student_data

def go_lab3(group:str) -> list:
    student_ids = get_students(group)
    if not student_ids:
        raise ValueError("Не найдены студенты")
    
    course_schedules = get_courses_schedules(group)
    if not course_schedules:
        raise ValueError("Не найдено расписание")
    
    courses = []
    for course_item in course_schedules:
        title = course_item[0]
        hours_info = get_students_hours(student_ids, course_item[1])
        planned = hours_info[0][2]
        students = []
        for item in hours_info:
            name, code = get_student_data(item[0])
            students.append({"fullname":name, "code":code, "valid_hours":item[1]})

        courses.append({"title":title, "planned_hours":planned, "students": students})

    return courses