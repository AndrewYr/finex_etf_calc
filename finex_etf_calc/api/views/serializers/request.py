from datetime import date

from pydantic import Field

from finex_etf_calc.db.models.funds import DealsSchema


class DealsSchemaReq(DealsSchema):
    id: int = Field(None)
    # type_id: int = Field(..., description='тип сделки id', examples=[1, 2])
    fund: str = Field(..., description='Название фонда', examples=['FXEM', 'FXRE'])
    count: int = Field(..., description='Количество покупки/продажи')
    price: float = Field(..., description='Цена сделки')
    date_deal: date = Field(..., description='Дата сделки', examples=[])


# TODO настроить валидацию на поля
# TODO Подумать на счет проверки добавления записи в БД, нужна ли проверка фонда
