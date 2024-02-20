import typing as t
from datetime import date

from pydantic import Field, ConfigDict, BaseModel, field_validator, model_validator, root_validator, validator

from finex_etf_calc.api.views.serializers.schemas import DealsSchema, TypesDealsSchema


class DealsSchemaResp(DealsSchema):
    model_config = ConfigDict(populate_by_name=True)

    type_deal: TypesDealsSchema = Field(None, alias='typeDeal')
    date_deal: date = Field(None, alias='dateDeal')


class FundSchemaResp(BaseModel):
    funds_ticker: str = Field(...)
    count: int = Field(...)
    currency: str = Field(...)
    price: float = Field(...)
    price_on_date: date = Field(..., validation_alias='price_date')
    price_in_rub: float = Field(..., validation_alias='in_rub')

    @field_validator('price')
    def price_check(cls, v):
        return round(v, 3)

    @field_validator('price_in_rub')
    def in_rub_check(cls, v):
        return round(v, 2)


class PricesSchemaResp(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    full_price_in_rub: float = Field(..., validation_alias='full_price')
    funds: t.List[FundSchemaResp] = Field(FundSchemaResp)

    @field_validator('full_price_in_rub')
    def full_price_in_rub_check(cls, v):
        return round(v, 2)

    @model_validator(mode='before')
    def calculate_full_price_in_rub(self):
        resp = {
            'funds': self,
            'full_price_in_rub': sum(fund.in_rub for fund in self)
        }
        return resp
