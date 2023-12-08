import logging
from typing import AsyncIterator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext import SQLAlchemyError

from finex_etf_calc.app.config import config

async_engine = create_async_engine(config['ASYNC_DB_URL'])
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    autoflush=False,
)
logger = logging.getLogger(config['APP_NAME'])


async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        yield AsyncSessionLocal
    except Exception as e:
        logger.exception(e)
