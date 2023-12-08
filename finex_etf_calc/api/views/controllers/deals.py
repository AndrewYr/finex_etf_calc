import typing as t

from finex_etf_calc.api.views.controllers.common import BaseController
from finex_etf_calc.db.models.funds import Deals, DealsSchema


class CreateDeals(BaseController):
    async def perform(self, deals: t.List[DealsSchema], *args, **kwargs):
        async with self.async_session as session:
            for deal in deals:
                new_deal = await Deals.create(session, deal)
                yield DealsSchema.model_validate(new_deal)
            await session.commit()


class GetDeals(BaseController):
    def perform(self, data):
        pass
