import typing as t
from datetime import datetime

from fastapi import HTTPException
from pydantic import ValidationError
from pydantic.tools import parse_obj_as

from finex_etf_calc.api.views.controllers.common import BaseController
from finex_etf_calc.db.models.funds import Deals
from finex_etf_calc.api.views.serializers.schemas import DealsSchema, PricesFundSchema
from finex_etf_calc.utils.adapters.deals import DealsAdapter
from finex_etf_calc.utils.adapters.prices_currency import PricesCurrencyAdapter
from finex_etf_calc.utils.adapters.prices_fund import PricesFundAdapter


class CreateDeals(BaseController):
    async def perform(self, deals: t.List[DealsSchema], *args, **kwargs) -> t.AsyncIterator[DealsSchema]:
        async with self.async_session as session:
            for deal in deals:
                new_deal = await Deals.create(session, deal)
                await session.refresh(new_deal)
                try:
                    yield DealsSchema.model_validate(new_deal)
                except ValidationError as exc:
                    raise HTTPException(status_code=400)

            await session.commit()


class GetDeals(BaseController):
    async def perform(self, *args, **kwargs):
        async with self.async_session as session:
            resp_funds_actual_count = await DealsAdapter.get_actual_count_funds(session)
            resp_actual_price_funds = await PricesFundAdapter.get_actual_price_funds(session, resp_funds_actual_count)

            resp_list = []
            for i, j in zip(
                    sorted(resp_funds_actual_count, key=lambda x: x['funds_ticker']),
                    sorted(resp_actual_price_funds, key=lambda x: x['funds_ticker']),
            ):
                actual_price_currency = await PricesCurrencyAdapter.last_price_currency_on_date(
                    session,
                    i['currency'],
                    datetime.today(),
                )
                i.update(j)
                i['result'] = j['price'] * i['count']
                i['in_rub'] = i['result'] * actual_price_currency[0].price
                resp_list.append(i)

            return parse_obj_as(t.List[PricesFundSchema], resp_list)
