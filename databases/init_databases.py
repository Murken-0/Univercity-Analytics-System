from postgres.scheme.init import init_posgres
from postgres.scheme.partitions import create_partitions

from postgres.data.unik_courses import insert_unik_courses
from postgres.data.students import insert_students
from postgres.data.schedule import insert_schedule
from postgres.data.group_course import insert_group_course
from postgres.data.classes import insert_classes
from postgres.data.class_materials import insert_class_materials
from postgres.data.attendances import insert_attendances

from noSQL_migrations.redis import migrate_redis
from noSQL_migrations.elastic import migrate_elastic
from noSQL_migrations.mongo import migrate_mongo
from noSQL_migrations.neo4j import migrate_neo4j

import os

os.chdir(os.path.join(os.getcwd(), 'databases'))

#postgres
init_posgres()
create_partitions()

insert_unik_courses()
insert_students()
insert_group_course()
insert_classes()
insert_class_materials()
insert_schedule()
insert_attendances()

#migrations
migrate_elastic()
migrate_mongo()
migrate_neo4j()
migrate_redis()

print("Базы данных проинициализированы")