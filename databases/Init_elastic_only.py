from noSQL_migrations.elastic import migrate_elastic
import os

os.chdir(os.path.join(os.getcwd(), 'databases'))

migrate_elastic()

print('ok')