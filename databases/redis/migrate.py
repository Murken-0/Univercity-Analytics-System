import psycopg2
import redis

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='practice',
    user='admin',
    password='admin'
)

cursor = conn.cursor()
query = "SELECT fullname, code FROM students"
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()

r = redis.Redis(
    host='localhost',
    port=6379,
)

# Добавляем данные в Redis
for row in rows:
    code = row[1]
    fullname = row[0]
    r.set(code, fullname)