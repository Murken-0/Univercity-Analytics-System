import os
from elastic import search_materials
from postgres import get_attended_percentage
from redis_query import get_student_data
from tabulate import tabulate

os.chdir('/home/murken/Docker/labs/lab1')
print('\n\n\n')

def go_lab1():
    phrase = input('Фраза для поиска: ')

    classes = search_materials(phrase)
    if not classes:
        print('Не найдено занятий с таким термином')
        return
    
    start_date = input('Дата начала (YYYY-MM-DD): ')
    end_date = input('Дата конца (YYYY-MM-DD): ')

    students_with_percent = get_attended_percentage(class_ids=classes, start_date=start_date, end_date=end_date)
    if not students_with_percent:
        print("Не найдено соответствующих занятий данном периоде")
        return
    
    formatted = [[get_student_data(info[0]), info[0], round(info[1], 1)] for info in students_with_percent]
    print(tabulate(formatted, headers=['Студент', 'Шифр', 'Процент посещения'], tablefmt="fancy_grid", showindex="always"))

go_lab1()