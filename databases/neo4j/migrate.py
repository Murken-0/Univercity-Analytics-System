import psycopg2
from py2neo import Graph, Node, Relationship

pg_conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
)

pg_cursor = pg_conn.cursor()
neo4j_graph = Graph("bolt://localhost:7687")

#departments
pg_cursor.execute("SELECT id, code, title FROM departments")
departments = pg_cursor.fetchall()

for department_node in departments:
    department_node = Node("Department", id=department_node[0], code=department_node[1], title=department_node[2])
    neo4j_graph.create(department_node)

#specialities
pg_cursor.execute("SELECT id, code, title FROM specialities")
specialities = pg_cursor.fetchall()

for speciality_node in specialities:
    speciality_node = Node("Speciality", id=speciality_node[0], code=speciality_node[1], title=speciality_node[2])
    neo4j_graph.create(speciality_node)

#dep_spec
pg_cursor.execute("SELECT department_id, speciality_id FROM department_speciality")
department_specialities = pg_cursor.fetchall()
for department_speciality in department_specialities:
    department_node = neo4j_graph.nodes.match("Department", id=department_speciality[0]).first()
    speciality_node = neo4j_graph.nodes.match("Speciality", id=department_speciality[1]).first()
    relationship = Relationship(department_node, "HAS_SPECIALITY", speciality_node)
    neo4j_graph.create(relationship)

#groups
pg_cursor.execute("SELECT id, title, department_id, speciality_id  FROM groups")
groups = pg_cursor.fetchall()
for group in groups:
    group_node = Node("Group", id=group[0], title=group[1])
    neo4j_graph.create(group_node)

    department_node = neo4j_graph.nodes.match("Department", id=group[2]).first()
    speciality_node = neo4j_graph.nodes.match("Speciality", id=group[3]).first()

    relationship_dep = Relationship(department_node, "OFFERS_GROUP", group_node)
    relationship_spec = Relationship(group_node, "HAS_SPECIALITY", speciality_node)

    neo4j_graph.create(relationship_dep)
    neo4j_graph.create(relationship_spec)

#students
pg_cursor.execute("SELECT id, fullname, code, group_id FROM students")
students = pg_cursor.fetchall()
for student in students:
    student_node = Node("Student", id=student[0], code=student[2])
    neo4j_graph.create(student_node)

    group_node = neo4j_graph.nodes.match("Group", id=student[3]).first()
    relationship = Relationship(student_node, "STUDY_IN", group_node)
    neo4j_graph.create(relationship)

#courses
pg_cursor.execute("SELECT id, title, scheduled_hours, department_id FROM courses")
courses = pg_cursor.fetchall()
for course in courses:
    course_node = Node("Course", id=course[0], code=course[2])
    neo4j_graph.create(course_node)

    department_node = neo4j_graph.nodes.match("Department", id=course[3]).first()
    relationship = Relationship(department_node, "HAS_COURSE", course_node)
    neo4j_graph.create(relationship)

#group_course
pg_cursor.execute("SELECT group_id, course_id, special FROM group_course")
group_courses = pg_cursor.fetchall()
for group_course in group_courses:
    group_node = neo4j_graph.nodes.match("Group", id=group_course[0]).first()
    course_node = neo4j_graph.nodes.match("Course", id=group_course[1]).first()
    relationship = Relationship(group_node, "STUDY_COURSE", course_node, special=group_course[2])
    neo4j_graph.create(relationship)

pg_cursor.close()
pg_conn.close()