from __future__ import with_statement
import sys
import os
from alembic import context
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from sqlalchemy.ext.declarative import declarative_base

# Adicione o caminho para o diretório do seu projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Base  # Importar o Base que contém suas definições de modelo

# Configurações do Alembic
config = context.config
config.set_main_option('sqlalchemy.url', 'postgresql://postgres:Sucesso15!@localhost/postgres')

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    connection = engine.connect()
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
