from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from config import settings


class DataBaseHelper:
    def __init__(self, url):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scope_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependebcy(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scope_session_dependebcy(self) -> AsyncSession:
        session = self.get_scope_session()
        yield session
        await session.close()


db_helper = DataBaseHelper(settings.db_url)


Base = declarative_base()
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)


# Зависимость для получения сессии базы данных
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
