import psycopg2
from py2neo import Graph, Node, Relationship

def migrate_neo4j():
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
    print("Neo4j | deparments перенесены")

    #specialities
    pg_cursor.execute("SELECT id, code, title FROM specialities")
    specialities = pg_cursor.fetchall()

    for speciality_node in specialities:
        speciality_node = Node("Speciality", id=speciality_node[0], code=speciality_node[1], title=speciality_node[2])
        neo4j_graph.create(speciality_node)
    print("Neo4j | specialities перенесены")

    #dep_spec
    pg_cursor.execute("SELECT department_id, speciality_id FROM department_speciality")
    department_specialities = pg_cursor.fetchall()
    for department_speciality in department_specialities:
        department_node = neo4j_graph.nodes.match("Department", id=department_speciality[0]).first()
        speciality_node = neo4j_graph.nodes.match("Speciality", id=department_speciality[1]).first()
        relationship = Relationship(department_node, "HAS_SPECIALITY", speciality_node)
        neo4j_graph.create(relationship)
    print("Neo4j | department_speciality перенесены")

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
    print("Neo4j | groups перенесены")

    #students
    pg_cursor.execute("SELECT id, fullname, code, group_id FROM students")
    students = pg_cursor.fetchall()
    for student in students:
        student_node = Node("Student", id=student[0], code=student[2])
        neo4j_graph.create(student_node)

        group_node = neo4j_graph.nodes.match("Group", id=student[3]).first()
        relationship = Relationship(student_node, "STUDY_IN", group_node)
        neo4j_graph.create(relationship)
    print("Neo4j | students перенесены")

    #courses
    pg_cursor.execute("SELECT id, title, scheduled_hours, department_id FROM courses")
    courses = pg_cursor.fetchall()
    for course in courses:
        course_node = Node("Course", id=course[0], title=course[1], hours=course[2])
        neo4j_graph.create(course_node)

        department_node = neo4j_graph.nodes.match("Department", id=course[3]).first()
        relationship = Relationship(department_node, "HAS_COURSE", course_node)
        neo4j_graph.create(relationship)
    print("Neo4j | courses перенесены")

    #group_course
    pg_cursor.execute("SELECT group_id, course_id, special FROM group_course")
    group_courses = pg_cursor.fetchall()
    for group_course in group_courses:
        group_node = neo4j_graph.nodes.match("Group", id=group_course[0]).first()
        course_node = neo4j_graph.nodes.match("Course", id=group_course[1]).first()
        relationship = Relationship(group_node, "STUDY_COURSE", course_node, special=group_course[2])
        neo4j_graph.create(relationship)
    print("Neo4j | group_course перенесены")

    #classes
    pg_cursor.execute("SELECT id, type_id, title, equipment, course_id FROM classes") 
    classes = pg_cursor.fetchall()
    for clas in classes:
        clas_node= Node("Class", id=clas[0], type='practice' if clas[1] == 1 else 'lection', title=clas[2], equipment=clas[3])
        neo4j_graph.create(clas_node)

        course_node = neo4j_graph.nodes.match("Course", id=clas[4]).first()
        relationship = Relationship(course_node, "HAS_CLASS", clas_node)
        neo4j_graph.create(relationship)
    print("Neo4j | classes перенесены")

    #schedule
    pg_cursor.execute("SELECT id, date, pair_number, class_id, group_id FROM schedule") 
    schedules = pg_cursor.fetchall()
    for schedule in schedules:
        date_time = schedule[1]
        schedule_node = Node("Schedule", id=schedule[0], date=date_time, pair_number=schedule[2])
        neo4j_graph.create(clas_node)

        clas_node = neo4j_graph.nodes.match("Class", id=schedule[3]).first()
        relationship = Relationship(schedule_node, "REFERS_TO_CLASS", clas_node)
        neo4j_graph.create(relationship)

        group_node = neo4j_graph.nodes.match("Group", id=schedule[4]).first()
        relationship = Relationship(schedule_node, "REFERS_TO_GROUP", group_node)
        neo4j_graph.create(relationship)
    print("Neo4j | schedule перенесены")

    pg_cursor.close()
    pg_conn.close()
    print("Neo4j | Миграция завершена")