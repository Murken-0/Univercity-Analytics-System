from py2neo import Graph

def get_students_and_shedule(classes:list) -> list:
    neo4j_graph = Graph("bolt://localhost:7687")
    info = [[], []]
    for cl in classes:
        find_students_schedule_query = f"MATCH (c:Class {{id:{cl}}})<-[:REFERS_TO_CLASS]-(s:Scheldue)-[:REFERS_TO_GROUP]->(g:Group)<-[:STUDY_IN]-(st:Student) RETURN st.id as students, s.id as schedules"
        result = neo4j_graph.run(find_students_schedule_query)
        for record in result:
            info[0].append(record['students'])
            info[1].append(record['schedules'])
    return info
