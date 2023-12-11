from py2neo import Graph

def get_courses_schedules(group:str) -> dict:
    neo4j_graph = Graph("bolt://localhost:7687")
    query = f"""MATCH (group:Group {{title: "{group}"}})-[:STUDY_COURSE {{special: True}}]->(course:Course)-[:HAS_CLASS]->(class:Class)<-[:REFERS_TO_CLASS]-(sch:Schedule)
RETURN course.title AS course_title, collect(sch.id) AS scheldue_ids"""
    result = neo4j_graph.run(query)

    return [[record["course_title"], record["scheldue_ids"]] for record in result]

def get_students(group:str) -> list:
    neo4j_graph = Graph("bolt://localhost:7687")
    query = f"""MATCH (g:Group {{title: "{group}"}})<-[:STUDY_IN]-(s:Student)
        RETURN s.id AS student_id"""
    result = neo4j_graph.run(query)

    return [record["student_id"] for record in result]

"""
MATCH (group:Group {title: "БСБО-01-20"})-[:STUDY_COURSE {special: True}]->(course:Course)-[:HAS_CLASS]->(class:Class)<-[:REFERS_TO_CLASS]-(sch:Schedule)
RETURN course.title AS course_title, collect(sch.id) AS scheldue_ids
"""

"""
MATCH (g:Group {title: "БСБО-01-20"})<-[:STUDY_IN]-(s:Student)
RETURN s.id AS student_id
"""