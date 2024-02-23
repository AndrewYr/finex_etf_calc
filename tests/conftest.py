from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from alembic.command import downgrade, upgrade

from finex_etf_calc.app.config import config
from finex_etf_calc.app.fastapi import create_app
from finex_etf_calc.db.models import Base


from sqlalchemy import create_engine
from alembic.config import Config as AlembicConfig
import pytest


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def async_client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(config.ALEMBIC_CONFIG)
    return engine


@pytest.fixture(scope="session")
def apply_migrations(db_engine):
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.attributes['configure_logger'] = False

    upgrade(alembic_cfg, 'head')
    yield 'on head'
    downgrade(alembic_cfg, 'base')

@pytest.fixture(scope="function")
def db_session(db_engine, apply_migrations):
    """Создание новой сессии для каждого теста."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def db_session_with_funds(db_engine, apply_migrations):
    """Создание новой сессии для каждого теста."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # TODO Поправить миграцию, БД создается но миграция почемуто не накатывается корректно
    # async with scoped_session() as session:
    #     await Funds.create(
    #         session=session,
    #         funds=FundsSchema(ticker='FXCN', currencies_name='USD'),
    #     )

    yield session

    session.close()
    transaction.rollback()
    connection.close()
