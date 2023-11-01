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

query = "SELECT class_id, file FROM class_materials"
cursor.execute(query)

rows = cursor.fetchall()

cursor.close()
conn.close()

es = Elasticsearch(
    hosts=['http://localhost:9200'], 
    timeout=30,
)

if not es.ping():
    print("Не удалось подключиться к Elasticsearch")
else:
    for row in rows:
        class_id = row[0]
        file = row[1]

        document = {
            'class_id': class_id,
            'file': file
        }

        es.index(index='materials', id=class_id, body=document)