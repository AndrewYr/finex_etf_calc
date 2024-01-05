import typing as t
from fastapi import APIRouter, Depends

from finex_etf_calc.api.views.controllers.deals import CreateDeals, GetDeals
from finex_etf_calc.api.views.serializers.request import DealsSchemaReq
from finex_etf_calc.api.views.serializers.response import DealsSchemaResp, PricesSchemaResp

routes = APIRouter()


@routes.get(
    '/prices',
    response_model=t.List[PricesSchemaResp],
    status_code=200,
    description='Получить актуальную сумму всех имеющихся фондов'
)
async def get_funds(
        controller: GetDeals = Depends(GetDeals)
):
    # TODO добавить общий результат на какуюто определенную валюту с пересчетом допустим на рубли
    return await controller.perform()


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
    return [deal async for deal in controller.perform(deals)]
