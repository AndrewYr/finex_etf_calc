import typing as t
from datetime import date

from pydantic import Field, ConfigDict, BaseModel, field_validator, model_validator, root_validator, validator

from finex_etf_calc.api.views.serializers.schemas import DealsSchema, TypesDealsSchema


class DealsSchemaResp(DealsSchema):
    model_config = ConfigDict(populate_by_name=True)

    type_deal: TypesDealsSchema = Field(None, alias='typeDeal')
    date_deal: date = Field(None, alias='dateDeal')


class FundSchemaResp(BaseModel):
    # model_config = ConfigDict(populate_by_name=True)

    funds_ticker: str = Field(...)
    count: int = Field(...)
    currency: str = Field(...)
    price: float = Field(...)
    result: float = Field(...)
    price_date: date = Field(...)
    in_rub: float = Field(...)

    @field_validator('result')
    def result_check(cls, v):
        return round(v, 2)

    # @field_validator('price')
    # def price_check(cls, v):
    #     return round(v, 2)

    @field_validator('in_rub')
    def in_rub_check(cls, v):
        return round(v, 2)


class PricesSchemaResp(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    full_price: float = Field(...)
    # currency: str = Field(...)
    funds: t.List[FundSchemaResp] = Field(FundSchemaResp)

    @field_validator('full_price')
    def full_price_check(cls, v):
        return round(v, 2)

    @model_validator(mode='before')
    def calculate_full_price_in_rub(self):
        resp = {
            'funds': self,
            'full_price': sum(fund.in_rub for fund in self)
        }
        return resp
