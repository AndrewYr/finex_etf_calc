from httpx import AsyncClient


async def test_get_actual_prices_response_empty(
        async_client: AsyncClient,
        db_session,
):
    response = await async_client.get('/v1/prices')
    assert response.status_code == 200
    assert response.json() == {
        'full_price_in_rub': 0.0,
        'funds': [],
    }


async def test_create_deals(
        async_client: AsyncClient,
        db_session,
):
    response = await async_client.post(
        '/v1/deals',
        json=[
            {
                'typeDeal': {
                    'name': 'buy',
                },
                'funds': {},
            }
        ],
    )
    assert response.status_code == 201
    assert response.json() == {
        'full_price_in_rub': 0.0,
        'funds': [],
    }
