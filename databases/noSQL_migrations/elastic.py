import psycopg2
from elasticsearch import Elasticsearch

def migrate_elastic():
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
        print("ElasticSearch | Не удалось подключиться ")
        return
    for row in rows:
        es.index(index='materials', id=row[0], body={
            'class_id': row[1],
            'file': row[2]
        })
    print("ElasticSearch | Миграция завершена")

migrate_elastic()