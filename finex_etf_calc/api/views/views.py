import typing as t
from fastapi import APIRouter, Depends

from finex_etf_calc.api.views.serializers.request import DealsSchemaReq

routes = APIRouter()


@routes.get(
    '/funds',
    response_model=t.List[dict],
    status_code=200,
    description='Получить актуальную сумму всех имеющихся фондов'
)
async def get_funds():
    pass


@routes.post(
    '/deals',
    response_model=t.List[dict],
    status_code=201,
    description='Создать запись о движении фондов (покупка/продажа)'
)
async def create_deals(
        deals: t.List[DealsSchemaReq],
        controller: CreateDeals = Depends(CreateDeals)
):
    pass


@routes.get('/deals', response_model=t.List[dict], status_code=200)
async def get_deals():
    pass
