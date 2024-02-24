#! /bin/bash

COMPONENT_DIR="/home/appuser"
CONNECT_PROPS="/etc/ksqldb-server/connect.properties"
CONFLUENT_HUB="/home/appuser/bin/confluent-hub"

$CONFLUENT_HUB install debezium/debezium-connector-postgresql:latest \
  --component-dir $COMPONENT_DIR \
  --worker-configs $CONNECT_PROPS \
  --no-prompt

$CONFLUENT_HUB install jcustenborder/kafka-connect-redis:latest \
  --component-dir $COMPONENT_DIR \
  --worker-configs $CONNECT_PROPS \
  --no-prompt

$CONFLUENT_HUB install confluentinc/kafka-connect-elasticsearch:latest \
  --component-dir $COMPONENT_DIR \
  --worker-configs $CONNECT_PROPS \
  --no-prompt

ksql-server-start /etc/ksqldb-server/ksql-server.properties