import psycopg2
from pymongo import MongoClient

pg_conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
)

mongo_client = MongoClient('mongodb://localhost:27017/', username='admin', password='admin', authSource='admin')
mongo_db = mongo_client["practice"]
mongo_collection = mongo_db["universities"]

cursor = pg_conn.cursor()
mongo_data = []

cursor.execute("SELECT id, title FROM universities")
universities = cursor.fetchall()
for unik in universities:
    university = {
        "title" : unik[1],
        "institutes" : []
    }
    cursor.execute(f"SELECT id, title FROM institutes WHERE university_id = {unik[0]}")
    institutes = cursor.fetchall()
    for inst in institutes:
        institute = {
            "title" : inst[1],
            "departments" : []
        }
        cursor.execute(f"SELECT code, title FROM departments WHERE institute_id = {inst[0]}")
        departments = cursor.fetchall()
        for dep in departments:
            department = {
                "code" : dep[0],
                "title" : dep[1]
            }
            institute["departments"].append(department)
        university["institutes"].append(institute)
    mongo_data.append(university)

mongo_collection.insert_many(mongo_data)    

cursor.close()
pg_conn.close()
mongo_client.close()
