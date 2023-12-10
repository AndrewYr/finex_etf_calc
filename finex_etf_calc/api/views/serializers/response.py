from datetime import date

from pydantic import Field, ConfigDict

from finex_etf_calc.db.models.funds import DealsSchema, TypesDealsSchema


class DealsSchemaResp(DealsSchema):
    model_config = ConfigDict(populate_by_name=True)

    type_deal: TypesDealsSchema = Field(None, alias='typeDeal')
    date_deal: date = Field(None, alias='dateDeal')
