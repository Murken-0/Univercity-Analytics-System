from SQL.scheme.init import init_posgres
from SQL.scheme.partitions import create_partitions

from SQL.data.unik_courses import insert_unik_courses
from SQL.data.students import insert_students
from SQL.data.schedule import insert_schedule
from SQL.data.group_course import insert_group_course
from SQL.data.classes import insert_classes
from SQL.data.class_materials import insert_class_materials
from SQL.data.attendances import insert_attendances

from noSQL.redis_migration import migrate_redis
from noSQL.elastic_migration import migrate_elastic
from noSQL.mongo_migration import migrate_mongo
from noSQL.neo4j_migration import migrate_neo4j

import os

os.chdir(os.path.join(os.getcwd(), 'databases'))

#postgres_scheme
#init_posgres()
#create_partitions()

#postgres_data
insert_unik_courses()
insert_students()
insert_group_course()
insert_classes()
insert_class_materials()
insert_schedule()
insert_attendances()

#migrations
#migrate_elastic()
#migrate_mongo()
#migrate_redis()
#migrate_neo4j()

print("Базы данных проинициализированы")