import os
from elastic import search_materials
from postgres import get_attended_percentage, get_schedule_by_classes
from redis_query import get_student_data
from neo4j import get_students_by_shedule
from tabulate import tabulate

os.chdir('/home/murken/docker/labs/lab1')
print('\n\n\n')

def go_lab1():
    phrase = input('Фраза для поиска: ')

    classes = search_materials(phrase)
    if not classes:
        print('Не найдено занятий с таким термином')
        return
    
    schedule_ids = [i[0] for i in get_schedule_by_classes(classes)]
    if not schedule_ids:
        print('Не найдено расписание для этого занятия')
        return
    student_ids = get_students_by_shedule(schedule_ids)
    if not student_ids:
        print('Не найдено студентов для этого занятия')
        return

    start_date = input('Дата начала (YYYY-MM-DD): ')
    end_date = input('Дата конца (YYYY-MM-DD): ')

    students_with_percent = get_attended_percentage(schedule_ids, student_ids, start_date, end_date)
    if not students_with_percent:
        print("Не найдено соответствующих занятий данном периоде")
        return
    
    formatted = []
    for info in students_with_percent:
        student = get_student_data(info[0])
        formatted.append([student["fullname"], student["code"], round(info[1], 2)])
    print(tabulate(formatted, headers=['Студент', 'Шифр', 'Процент посещения'], tablefmt="fancy_grid", showindex="always"))

go_lab1()