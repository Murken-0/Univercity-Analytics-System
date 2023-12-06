import os
from elastic import search_materials
from postgres import get_attended_percentage, get_schedule_by_classes
from redis_query import get_student_data
from neo4j import get_students_and_shedule
from tabulate import tabulate

os.chdir('/home/murken/docker/labs/lab1')
print('\n\n\n')

def go_lab1():
    phrase = input('Фраза для поиска: ')

    classes = search_materials(phrase)
    if not classes:
        print('Не найдено занятий с таким термином')
        return

    start_date = input('Дата начала (YYYY-MM-DD): ')
    end_date = input('Дата конца (YYYY-MM-DD): ')
    
    info = get_students_and_shedule(classes)
    if not info:
        print('Не найдено расписание для занятий')
        return

    students_with_percent = get_attended_percentage(info, start_date, end_date)
    if not students_with_percent:
        print("Ошибка с расчетом процента почещения")
        return
    
    formatted = []
    for info in students_with_percent:
        student_info = get_student_data(info[0])
        formatted.append([student_info[0], student_info[1], round(info[1], 2)])
    print(tabulate(formatted, headers=['Студент', 'Шифр', 'Процент посещения'], tablefmt="fancy_grid", showindex="always"))

go_lab1()