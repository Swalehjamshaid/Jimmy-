
from __future__ import with_statement
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
config = context.config
fileConfig(config.config_file_name)
url = os.getenv('DATABASE_URL', config.get_main_option('sqlalchemy.url'))
if url.startswith('postgresql://'):
    url = url.replace('postgresql://','postgresql+psycopg2://')
config.set_main_option('sqlalchemy.url', url)

def run_migrations_offline():
    context.configure(url=url, literal_binds=True, dialect_opts={'paramstyle':'named'})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
