#postgres
curl -X POST -H "Content-Type: application/json" --data @connector-config/postgres-source.json http://localhost:8083/connectors &

#elastic
#curl -X POST -H "Content-Type: application/json" --data @connector-config/elasticsearch-sink.json http://localhost:8083/connectors &

#elastic-logs
#curl -X POST -H "Content-Type: application/json" --data @connector-config/elasticsearch-sink-all.json http://localhost:8083/connectors &

#neo4j
#curl -X POST -H "Content-Type: application/json" --data @connector-config/neo4j-sink.json http://localhost:8083/connectors &

#redis
#curl -X POST -H "Content-Type: application/json" --data @connector-config/redis-sink.json http://localhost:8083/connectors &

#mongo
curl -X POST -H "Content-Type: application/json" --data @connector-config/mongo-sink.json http://localhost:8083/connectors