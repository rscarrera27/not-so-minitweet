from infrastructure.database.tables import metadata, TweetTable
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import pytest


@pytest.fixture
async def postgres_session(postgresql, postgresql_proc):
    connection = f'postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    engine = create_async_engine(connection, echo=False, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
