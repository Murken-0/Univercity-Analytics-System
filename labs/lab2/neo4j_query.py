from py2neo import Graph

def get_class_volumes(title:str, start_date:str, end_date:str) -> list:
    neo4j_graph = Graph("bolt://localhost:7687")
    query = f"""MATCH (c:Course {{title: "{title}"}})-[:HAS_CLASS]->(cl:Class {{equipment: True}})<-[:REFERS_TO_CLASS]-(sch:Schedule)-[:REFERS_TO_GROUP]->(g:Group)<-[:STUDY_IN]-(s:Student) 
        WHERE sch.date >= date("{start_date}") AND sch.date <= date("{end_date}") 
        WITH cl.title as class_title, sch.date as date ,sch.pair_number AS pair_number, count(DISTINCT s) AS student_count
        RETURN class_title, date, pair_number, student_count"""
    result = neo4j_graph.run(query)

    info = [[], [], [], []]
    for record in result:
        info[0].append(record["class_title"])
        info[1].append(str(record["date"]))
        info[2].append(record["pair_number"])
        info[3].append(record["student_count"])
    return info