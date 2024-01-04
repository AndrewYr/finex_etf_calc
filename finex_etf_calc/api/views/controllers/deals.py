import typing as t

from fastapi import HTTPException
from pydantic import ValidationError

from finex_etf_calc.api.views.controllers.common import BaseController
from finex_etf_calc.db.models.funds import Deals
from finex_etf_calc.api.views.serializers.schemas import DealsSchema
from finex_etf_calc.utils.models.fund_deals import FundDeals
from finex_etf_calc.utils.models.prices_fund import PricesFundAdapter


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


class GetFundDeals(BaseController):
    async def perform(self, *args, **kwargs):
        async with self.async_session as session:
            res_lst_funds = await FundDeals.get_actual_count_funds(session)
            await PricesFundAdapter.fill_actual_price_funds(session, res_lst_funds)
            return res_lst_funds
