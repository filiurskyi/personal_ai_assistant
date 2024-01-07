import contextlib
import logging

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from fastapi_app.conf.config import DB_URI, OPENAI_API_KEY


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as e:
            logging.error("Failed to connect to database. Error: ", e)
            await session.rollback()
        finally:
            await session.close()


session_manager = DatabaseSessionManager(DB_URI)


async def get_db():
    async with session_manager.session() as session:
        yield session
