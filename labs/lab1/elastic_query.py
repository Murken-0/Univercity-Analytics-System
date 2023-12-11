from elasticsearch import Elasticsearch

def search_materials(user_input:str) -> list:
    es = Elasticsearch(
        hosts=['http://localhost:9200']
    )

    query = {
        "size": 10000,
        "query": {
            "match": {
                "file": f"{user_input}"
            }
        }
    }
    result = es.search(index='materials', body=query)
    return [hit['_source']['class_id'] for hit in result['hits']['hits']]