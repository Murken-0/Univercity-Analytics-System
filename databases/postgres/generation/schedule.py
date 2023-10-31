import random
from datetime import datetime, timedelta
import psycopg2

"""
descriptions = ['Агентство по информационной безопасности', 'Аутсорсинг', 
'Аутентификация', 'Биг дата', 'Бизнес-анализ', 'Веб-разработка', 'Глубокое обучение', 
'Девопс', 'Девелопер', 'Дизайн интерфейса', 'Дизайн пользовательского опыта', 'Кодировка', 
'Компьютерный вирус', 'Криптовалюта', 'Машинное обучение', 'Мобильная разработка', 'Облачные вычисления', 
'Программное обеспечение', 'Разработка программного обеспечения', 'Сетевая безопасность', 'Системное администрирование', 
'Социальные сети', 'Системный анализ', 'Системный архитектор', 'Сбор и анализ данных', 'Специалист по информационной безопасности', 
'Стартап', 'Тестирование программного обеспечения', 'Управление проектами', 'Фронтенд-разработка', 'Хакерская атака']

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

cursor.execute('SELECT id, scheduled_hours FROM courses')
courses = cursor.fetchall()

connection.close()

query = f"INSERT INTO lessons (type, date, description, equipment, course_id) VALUES "
for course in courses:
    course_id = course[0]
    scheduled_hours = course[1]

    start_date = datetime.strptime("2022-02-07", '%Y-%m-%d')
    end_date = datetime.strptime("2022-06-11", '%Y-%m-%d')
    
    delta = int((end_date - start_date).days / scheduled_hours)

    dates = [start_date + timedelta(days=i * delta) for i in range(scheduled_hours)]
    
    for date in dates:
        type = random.choice(['practice', 'lection'])
        description = ' '.join([random.choice(descriptions) for _ in range(random.randint(1, 5))])
        equipment = ' '.join([random.choice(descriptions) for _ in range(random.randint(1, 5))])
        
        query += f"\n('{type}', '{date}', '{description}', '{equipment}', {course_id}), "

with open("insert_classes.sql", "a") as file:
    file.write(query)
"""
start_date = datetime.strptime("2022-02-07", '%Y-%m-%d')
end_date = datetime.strptime("2022-06-11", '%Y-%m-%d')
delta = int((end_date - start_date).days / 16)
dates = [start_date + timedelta(days=i * delta) for i in range(16)]

connection = psycopg2.connect(host='localhost', port='5432', dbname='practice', user='admin', password='admin')
cursor = connection.cursor()
query = f"INSERT INTO schedule (class_id, group_id, date, pair_number) VALUES "

for course_id in range(1, 49):
    cursor.execute(f"SELECT id FROM classes WHERE course_id = {course_id}")
    classes = [cl[0] for cl in cursor.fetchall()]
    for i, cl in enumerate(classes):
        cursor.execute(f"SELECT groups.id FROM classes JOIN courses ON classes.course_id = courses.id JOIN group_course ON group_course.course_id = courses.id JOIN groups ON group_course.group_id = groups.id WHERE classes.id = {cl}")
        groups = [gr[0] for gr in cursor.fetchall()]
        for gr in groups:
            pair = random.randint(1,6)
            query += f"\n({cl}, {gr}, '{dates[i]}', {pair}),"

with open("sheldue.sql", "w") as file:
    file.write(query)

connection.close()