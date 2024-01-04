from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class TypesDealsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(None)


class FundsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    ticker: str = Field(None)
    currencies_name: str = Field(None, alias='currenciesName')


class DealsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(None)
    type_deal: TypesDealsSchema = Field(None)
    funds: FundsSchema = Field(None)
    count: int = Field(None)
    price: float = Field(None)
    date_deal: date = Field(None)


class PricesFundSchema(BaseModel):
    funds_ticker: str = Field(...)
    price_date: date = Field(...)
    price: float = Field(...)

# TODO возможно нужно переименовать файл
