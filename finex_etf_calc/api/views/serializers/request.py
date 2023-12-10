from datetime import date

from pydantic import Field

from finex_etf_calc.db.models.funds import DealsSchema, TypesDealsSchema


class DealsSchemaReq(DealsSchema):
    id: int = Field(None)
    type_deal: TypesDealsSchema = Field(None, alias='typeDeal')
    date_deal: date = Field(None, alias='dateDeal')


# TODO настроить валидацию на поля
# TODO Подумать на счет проверки добавления записи в БД, нужна ли проверка фонда
