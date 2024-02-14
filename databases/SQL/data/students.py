import random
import string
import psycopg2

def insert_students():
    surnames = ["Иванов", "Петров", "Сидоров", "Смирнов", "Васильев"]
    names = ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей"]
    patronymics = ["Иванович", "Петрович", "Алексеевич", "Дмитриевич", "Сергеевич"]

    connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM groups")
    groups = [i[0] for i in cursor.fetchall()]

    query = "INSERT INTO students (fullname, code, group_id) VALUES\n"
    for _ in range(500):
        surname = random.choice(surnames)
        name = random.choice(names)
        patronymic = random.choice(patronymics)
        student_id = generate_student_id()
        group_id = random.choice(groups)

        query += f"('{surname} {name} {patronymic}', '{student_id}', {group_id}),\n"
    query = query[:-2]

    cursor.execute(query)
    connection.commit()
    connection.close()

    with open("SQL/data/sql/students.sql", "w") as file:
        file.write(query + ';')

    print('Postgres | Таблица students заполнена')

def generate_student_id():
    digits = string.digits
    russian_letters = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЮЯ"

    student_id = ""
    for _ in range(6):
        symbol_type = random.randint(0, 1)
        if symbol_type == 0:
            symbol = random.choice(digits)
        else:
            symbol = random.choice(russian_letters)

        student_id += symbol

    return student_id