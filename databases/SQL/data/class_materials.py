import random
import psycopg2

def insert_class_materials():
    materials = ['Агентство по информационной безопасности', 'Аутсорсинг', 
    'Аутентификация', 'Биг дата', 'Бизнес-анализ', 'Веб-разработка', 'Глубокое обучение', 
    'Девопс', 'Девелопер', 'Дизайн интерфейса', 'Дизайн пользовательского опыта', 'Кодировка', 
    'Компьютерный вирус', 'Криптовалюта', 'Машинное обучение', 'Мобильная разработка', 'Облачные вычисления', 
    'Программное обеспечение', 'Разработка программного обеспечения', 'Сетевая безопасность', 'Системное администрирование', 
    'Социальные сети', 'Системный анализ', 'Системный архитектор', 'Сбор и анализ данных', 'Специалист по информационной безопасности', 
    'Стартап', 'Тестирование программного обеспечения', 'Управление проектами', 'Фронтенд-разработка', 'Хакерская атака']

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="practice",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM classes")
    classes = [i[0] for i in cursor.fetchall()]

    query = 'INSERT INTO class_materials(class_id, file) VALUES\n'
    for cl in classes:
        for _ in range(1, random.randint(2, 3)):
            text = ' '.join([random.choice(materials) for _ in range(random.randint(3, 15))])
            query += f"({cl}, '{text}'),\n"
    query = query[:-2]

    cursor.execute(query)
    connection.commit()
    connection.close()

    with open("SQL/data/sql/class_materials.sql", "w") as file:
        file.write(query+ ';')

    print('Postgres | Таблица class_materials заполнена')