from py2neo import Graph

def get_students_and_shedule(classes:list) -> list:
    neo4j_graph = Graph("bolt://neo4j:7687")
    students = []
    schedules = []
    for cl in classes:
        query = f"""MATCH (c:Class {{id:{cl}}})<-[:REFERS_TO_CLASS]-(s:Schedule)-[:REFERS_TO_GROUP]->(g:Group)<-[:STUDY_IN]-(st:Student) 
                    RETURN st.id as students, s.id as schedules"""
        result = neo4j_graph.run(query)
        for record in result:
            students.append(record['students'])
            schedules.append(record['schedules'])
    return students, schedules
