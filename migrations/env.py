import asyncio
from logging.config import fileConfig
from typing import Iterable, List, Optional, Union, no_type_check

import nest_asyncio  # type: ignore
from alembic import context
from alembic.operations.ops import MigrationScript
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from src.core import load_settings
from src.database.models import Base

target_metadata = Base.metadata

config = context.config
config.set_main_option("sqlalchemy.url", load_settings().db.url)

fileConfig(config.config_file_name)  # type: ignore


def add_number_to_migrations(
    context: MigrationContext,
    revision: Union[str, Iterable[Optional[str]]],
    directives: List[MigrationScript],
) -> None:
    migration_script = directives[0]
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()  # type: ignore
    if head_revision is None:
        new_rev_id = 1
    else:
        last_rev_id = int(head_revision.split("_")[0])
        new_rev_id = last_rev_id + 1
    migration_script.rev_id = f"{new_rev_id:02}_{migration_script.rev_id}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_server_default=True,
        render_as_batch=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


@no_type_check
def do_run_migrations(connection: AsyncConnection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_server_default=True,
        compare_type=True,
        render_as_batch=True,
        include_schemas=True,
        process_revision_directives=add_number_to_migrations,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),  # type: ignore
            prefix="sqlalchemy.",  # noqa
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(run_migrations_online())
