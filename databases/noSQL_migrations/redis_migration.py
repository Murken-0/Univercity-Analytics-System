import psycopg2
from redis import Redis

def migrate_redis():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='practice',
        user='admin',
        password='admin'
    )

    cursor = conn.cursor()
    query = "SELECT id, fullname, code FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    cursor.close()
    conn.close()

    redis = Redis(
        host='localhost',
        port=6379,
    )

    for student in students:
        redis.hset(student[0], mapping ={"fullname": student[1], "code":student[2]})
    print("Redis | Миграция завершена")