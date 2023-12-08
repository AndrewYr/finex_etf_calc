import typing as t
from fastapi import APIRouter, Depends

from finex_etf_calc.api.views.controllers.deals import CreateDeals
from finex_etf_calc.api.views.serializers.request import DealsSchemaReq

routes = APIRouter()


# @routes.get(
#     '/funds',
#     response_model=t.List[dict],
#     status_code=200,
#     description='Получить актуальную сумму всех имеющихся фондов'
# )
# async def get_funds(
#         controller: GetDeals = Depends(GetDeals)
# ):
#     return [GetDeals.get()]
# from pydantic import Field, BaseModel
# class A(BaseModel):
#     id: int = Field(None)


@routes.post(
    '/deals',
    response_model=t.List[dict],
    status_code=201,
    description='Создать запись о движении фондов (покупка/продажа)'
)
async def create_deals(
        deals: t.List[DealsSchemaReq],
        controller: CreateDeals = Depends(t.Optional[CreateDeals])
):
    return [deal async for deal in controller.perform(deals)]
