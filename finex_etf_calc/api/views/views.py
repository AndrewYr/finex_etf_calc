import typing as t
from fastapi import APIRouter, Depends

from finex_etf_calc.api.views.controllers.deals import CreateDeals
from finex_etf_calc.api.views.serializers.request import DealsSchemaReq
from finex_etf_calc.api.views.serializers.response import DealsSchemaResp

routes = APIRouter()


@routes.get(
    '/funds',
    response_model=t.List[dict],
    status_code=200,
    description='Получить актуальную сумму всех имеющихся фондов'
)
async def get_funds(
):
    return []


@routes.post(
    '/deals',
    response_model=t.List[DealsSchemaResp],
    status_code=201,
    description='Создать запись о движении фондов (покупка/продажа)'
)
async def create_deals(
        deals: t.List[DealsSchemaReq],
        controller: CreateDeals = Depends(CreateDeals)
):
    res = [deal async for deal in controller.perform(deals)]
    return res
