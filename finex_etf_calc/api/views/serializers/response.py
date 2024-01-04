from datetime import date

from pydantic import Field, ConfigDict, BaseModel

from finex_etf_calc.api.views.serializers.schemas import DealsSchema, TypesDealsSchema


class DealsSchemaResp(DealsSchema):
    model_config = ConfigDict(populate_by_name=True)

    type_deal: TypesDealsSchema = Field(None, alias='typeDeal')
    date_deal: date = Field(None, alias='dateDeal')


class PricesSchemaResp(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    funds_ticker: str = Field(..., alias='fundsTicker')
    count: int = Field(...)
    currency: str = Field(...)
    price: float = Field(...)
    result: float = Field(...)
    price_date: date = Field(..., alias='priceDate')
