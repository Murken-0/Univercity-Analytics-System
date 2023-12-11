from elastic_query import search_materials
from postgres_query import get_attended_percentage
from redis_query import get_student_data
from neo4j_query import get_students_and_shedule

def go_lab1(phrase, start_date, end_date):
    classes = search_materials(phrase)
    if not classes:
        raise ValueError('Не найдено занятий с таким термином')
    
    students, schedules = get_students_and_shedule(classes)
    if not students:
        raise ValueError('Не найдены студенты')
    if not schedules:
        raise ValueError('Не найдено расписание')

    students_with_percent = get_attended_percentage(students, schedules, start_date, end_date)
    if not students_with_percent:
        raise ValueError("Ошибка с расчетом процента почещения")
    
    result = []
    for student_info in students_with_percent:
        name, code = get_student_data(student_info[0])
        result.append([name, code, round(student_info[1], 2)])

    return result