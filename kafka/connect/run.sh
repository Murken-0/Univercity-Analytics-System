#! /bin/bash

COMPONENT_DIR="/home/appuser"

confluent-hub install debezium/debezium-connector-postgresql:latest \
  --component-dir $COMPONENT_DIR \
  --no-prompt

confluent-hub install confluentinc/kafka-connect-elasticsearch:latest \
  --component-dir $COMPONENT_DIR \
  --no-prompt

confluent-hub install neo4j/kafka-connect-neo4j:latest \
  --component-dir $COMPONENT_DIR \
  --no-prompt

cp /etc/connect/kafka-connect-redis-assembly-6.0.3.jar $COMPONENT_DIR/kafka-connect-redis-assembly-6.0.3.jar
cp /etc/connect/mongo-cdc-connector.jar $COMPONENT_DIR/mongo-cdc-connector.jar

/etc/confluent/docker/run & 
echo "Waiting for Kafka Connect to start listening on kafka-connect ⏳"
while [ $$(curl -s -o /dev/null -w %{http_code} http://connect:8083/connectors) -eq 000 ] ; do 
  echo -e $$(date) " Kafka Connect listener HTTP state: " $$(curl -s -o /dev/null -w %{http_code} http://kafka-connect:8083/connectors) " (waiting for 200)"
  sleep 5 
done
nc -vz connect 8083
/run-connectors.sh 
sleep infinity