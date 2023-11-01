import random
import psycopg2

def insert_classes():
    equipments = ['Ноутбук', 'Проектор', 'Интерактивная доска', 'Лабораторный стол', 'Сервер', 
    '3D-принтер', 'Робототехнический комплект', 'Электронный осциллограф', 'Шлем виртуальной реальности']

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM courses")
    courses = [i[0] for i in cursor.fetchall()]

    query = 'INSERT INTO classes(type_id, title, equipment, course_id) VALUES\n'
    for course in courses:
        l_eq = ' '.join([random.choice(equipments) for _ in range(random.randint(1, 5))])
        p_eq = ' '.join([random.choice(equipments) for _ in range(random.randint(1, 5))])
        for i in range(1, 9):
            l_name = f"Лекция {i}"
            query += f"(2, '{l_name}', '{l_eq}', {course}),\n"
            p_name = f"Практика {i}"
            query += f"(1, '{p_name}', '{p_eq}', {course}),\n"
    query = query[:-2]

    cursor.execute(query)
    connection.commit()
    connection.close()

    with open("postgres/data/sql/classes.sql", "w") as file:
        file.write(query+ ';')
    
    print('Postgres | Таблица classes заполнена')