import psycopg2
from elasticsearch import Elasticsearch

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='practice',
    user='admin',
    password='admin'
)

cursor = conn.cursor()

query = "SELECT id, class_id, file FROM class_materials"
cursor.execute(query)

rows = cursor.fetchall()

cursor.close()
conn.close()
es = Elasticsearch(
    hosts=['http://localhost:9200'], 
    request_timeout=5,
)

if not es.ping():
    print("Не удалось подключиться к Elasticsearch")
else:
    print("Успешное подключение к Elasticsearch")
    for row in rows:
        id = row[0]
        class_id = row[1]
        file = row[2]
        document = {
            'class_id': class_id,
            'file': file
        }
        es.index(index='materials', id=id, body=document)