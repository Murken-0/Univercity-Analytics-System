from py2neo import Graph, Node, Relationship

def get_students_by_shedule(schedule_ids:list) -> list:
    neo4j_graph = Graph("bolt://localhost:7687")
    students_data = []
    for sch in schedule_ids:
        schedule_id = sch
        find_students_query = f"MATCH (s:Scheldue {{id:{schedule_id}}})-[:REFERS_TO_GROUP]->(g:Group)<-[:STUDY_IN]-(st:Student) RETURN st.id as student_id"
        students = neo4j_graph.run(find_students_query)
        students_data.extend([student["student_id"] for student in students])
    return students_data
