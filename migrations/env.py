import os

from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.models import Base


# ############## REVISION & UPGRADE COMMANDS ############## #

# sample revision & upgrade command given relative path to alembic.ini
# alembic -c .\migrations\alembic.ini revision --autogenerate -m 'users teams projects'
# alembic -c .\migrations\alembic.ini upgrade head


# #################### RETRIEVE DB_URL #################### #

# def get_url():
#     user = os.getenv('POSTGRES_USER', 'postgres')
#     password = os.getenv('POSTGRES_PASSWORD', '')
#     host = os.getenv('POSTGRES_HOST', 'db')
#     db = os.getenv('POSTGRES_DB', 'app')
#     return f'postgresql://{user}:{password}@{host}/{db}'


# ######################## LOGGING ######################## #

# Interpret the config file for Python logging. This line sets up loggers basically.
config = context.config
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=os.getenv('DB_URL', 'sqlite:///app.db'),    # updated
        target_metadata=target_metadata,                # updated
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # added -> update configuration to include the correct db_url
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = os.getenv('DB_URL', 'sqlite:///app.db')
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
