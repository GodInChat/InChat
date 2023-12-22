import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.inchat.database.sql.models import Base, User
from src.config import settings


class Postgres:
    def __init__(self):
        user = settings.postgres_user
        pwd = settings.postgres_password
        host = settings.postgres_host
        port = settings.postgres_port
        db = settings.postgres_db
        url = (
            f"postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{db}?async_fallback=True"
        )

        self.engine = create_async_engine(url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        print("POSTGRES_CONNECTOR_INITIALIZED")

    async def __call__(self):
        async with self.async_session() as session:
            yield session

    async def create_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


    async def drop_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


database = Postgres()

async def get_user_db(session: AsyncSession = Depends(database)):
    yield SQLAlchemyUserDatabase(session, User)

async def main():
    await database.create_database()


if __name__ == "__main__":
    asyncio.run(main())
