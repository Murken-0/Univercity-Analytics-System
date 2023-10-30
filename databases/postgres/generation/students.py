import random
import string

def generate_student_data():
    surnames = ["Иванов", "Петров", "Сидоров", "Смирнов", "Васильев"]
    names = ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей"]
    patronymics = ["Иванович", "Петрович", "Алексеевич", "Дмитриевич", "Сергеевич"]

    insert_query = "INSERT INTO students (fullname, code, group_id) VALUES\n"
    for _ in range(500):
        surname = random.choice(surnames)
        name = random.choice(names)
        patronymic = random.choice(patronymics)
        student_id = generate_student_id()
        group_id = random.randint(16, 30)

        insert_query += f"('{surname} {name} {patronymic}', '{student_id}', {group_id}), \n"

    filename = "students.sql"
    with open(filename, "w") as file:
        file.write(insert_query)

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

generate_student_data()