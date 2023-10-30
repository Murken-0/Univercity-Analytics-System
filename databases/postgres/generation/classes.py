import random

equipments = ['Ноутбук', 'Проектор', 'Интерактивная доска', 'Лабораторный стол', 'Сервер', 
'3D-принтер', 'Робототехнический комплект', 'Электронный осциллограф', 'Шлем виртуальной реальности']

file = open('classes.sql', 'w')

query = 'INSERT INTO classes(type_id, title, equipment, course_id) VALUES\n'
for course in range(1, 49):
    l_eq = ' '.join([random.choice(equipments) for _ in range(random.randint(1, 5))])
    p_eq = ' '.join([random.choice(equipments) for _ in range(random.randint(1, 5))])
    for i in range(1, 9):
        l_name = f"Лекция {i}"
        query += f"(2, '{l_name}', '{l_eq}', {course}),\n"
        p_name = f"Практика {i}"
        query += f"(1, '{p_name}', '{p_eq}', {course}),\n"

file.write(query)
file.close()