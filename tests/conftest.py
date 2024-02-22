import pytest
from httpx import AsyncClient

from finex_etf_calc.app.fastapi import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def async_client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
