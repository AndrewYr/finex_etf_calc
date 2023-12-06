from datetime import date

from pydantic import Field, BaseModel


# TODO настроить валидацию на поля
# TODO Подумать на счет проверки добавления записи в БД, нужна ли проверка фонда
class DealsSchemaReq(BaseModel):
    class Config:
        orm_mode = True

    id: int = Field(None)
    type: str = Field(..., description='тип сделки', examples=['sell', 'bye'])
    fund: str = Field(..., description='Название фонда', examples=['FXEM', 'FXRE'])
    count: int = Field(..., description='Количество покупки/продажи')
    price: float = Field(..., description='Цена сделки')
    date: date = Field(..., description='Дата сделки', examples=[])
