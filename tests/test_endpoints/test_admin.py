from httpx import AsyncClient
from unittest.mock import patch, Mock


async def test_health_check(async_client: AsyncClient):
    response = await async_client.get('/v1/health')
    assert response.status_code == 200


@patch('finex_etf_calc.app.celery.app.send_task')
async def test_admin_funds_prices(
        send_task_mock: Mock,
        async_client: AsyncClient,
 ):
    send_task_mock.return_value = None
    response = await async_client.post('/admin/v1/funds/prices')
    assert response.status_code == 200
    assert send_task_mock.called
    assert send_task_mock.call_args[0][0] == 'tasks.full_load_prices_funds'


@patch('finex_etf_calc.app.celery.app.send_task')
async def test_admin_currencies_prices(
        send_task_mock: Mock,
        async_client: AsyncClient,
 ):
    send_task_mock.return_value = None
    response = await async_client.post('/admin/v1/currencies/prices')
    assert response.status_code == 200
    assert send_task_mock.called
    assert send_task_mock.call_args[0][0] == 'tasks.full_load_prices_currency'
