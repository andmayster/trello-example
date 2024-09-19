import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.exc import OperationalError

from core.models import Base

ENVIRONMENT = os.getenv('ENVIRONMENT')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')

# if ENVIRONMENT == "local":
# connection_string_local = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@localhost:5434/{POSTGRES_DBNAME}'
# else:
# connection_string_docker = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@postgresql:{POSTGRES_PORT}/{POSTGRES_DBNAME}'

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# print(connection_string)
config = context.config
# config.set_main_option('sqlalchemy.url', connection_string)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # try:
        # url = connection_string_local
    url = config.get_main_option("sqlalchemy.url")
    # url = connection_string_local
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()
    # except OperationalError:
    # url = connection_string_docker
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    # Пробуем подключиться по основному URL
    try:
        # URL по умолчанию (для Docker-среды)
        config.set_main_option("sqlalchemy.url",
                               f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@postgresql:{POSTGRES_PORT}/{POSTGRES_DBNAME}')
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()

    # Если подключение не удалось, пробуем другой URL
    except OperationalError as e:
        print(f"Primary connection failed: {e}. Trying alternative connection.")

        try:
            config.set_main_option("sqlalchemy.url",
                                   f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@localhost:5434/{POSTGRES_DBNAME}')
            connectable = engine_from_config(
                config.get_section(config.config_ini_section, {}),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )

            with connectable.connect() as connection:
                context.configure(
                    connection=connection, target_metadata=target_metadata
                )

                with context.begin_transaction():
                    context.run_migrations()

        except OperationalError as e:
            print(f"Alternative connection also failed: {e}")
            raise e


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
