CREATE SOURCE CONNECTOR postrges_source_connector
WITH (
  'connector.class' = 'io.debezium.connector.postgresql.PostgresConnector',
  'database.dbname' = 'practice',
  'database.history.kafka.bootstrap.servers' = 'kafka:9092',
  'database.hostname' = 'postgres',
  'database.password' = 'admin',
  'database.port' = '5432',
  'database.server.name' = 'postgres',
  'database.user' = 'admin',
  'plugin.name' = 'pgoutput',
  'tasks.max' = '1',
  'topic.creation.default.cleanup.policy' = 'delete',
  'topic.creation.default.partitions' = '1',
  'topic.creation.default.replication.factor' = '1',
  'topic.creation.default.retention.ms' = '604800000',
  'topic.creation.enable' = 'true',
  'topic.prefix' = 'postgres',
  'transforms' = 'route',
  'transforms.route.type' = 'io.debezium.transforms.ByLogicalTableRouter',
  'transforms.route.topic.regex' = 'public.(.*)',
  'transforms.route.topic.replacement' = '$1'
);

CREATE SINK CONNECTOR redis_sink WITH (
  'connector.class' = 'com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector',
  'tasks.max' = '1',
  'topics' = 'postgres.public.students',
  'redis.hosts' = 'redis:6379',
  'key.converter' = 'org.apache.kafka.connect.storage.StringConverter',
  'value.converter' = 'org.apache.kafka.connect.storage.StringConverter'
);