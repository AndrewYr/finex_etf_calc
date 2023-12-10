import logging
from typing import AsyncIterator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from finex_etf_calc.app.config import config

async_engine = create_async_engine(config['ASYNC_DB_URL'])
AsyncSessionMaker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)
logger = logging.getLogger(config['APP_NAME'])


async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        yield AsyncSessionMaker.begin()
    except Exception as e:
        logger.exception(e)
