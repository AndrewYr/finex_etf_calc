import logging
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session

from finex_etf_calc.app.config import config

async_engine = create_async_engine(
    config.ASYNC_DB_URL,
    echo=True,
)
AsyncSessionMaker = async_sessionmaker(
    async_engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)
logger = logging.getLogger(config.APP_NAME)


async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        async with AsyncSessionMaker() as session:
            yield session
    except Exception as e:
        logger.exception(e)


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        AsyncSessionMaker,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()
