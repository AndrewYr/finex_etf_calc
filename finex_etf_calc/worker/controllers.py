import os
from datetime import datetime

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from finex_etf_calc.app.config import config
from finex_etf_calc.db.engine import scoped_session
from finex_etf_calc.db.models.funds import Funds, PricesFund
from finex_etf_calc.api.views.serializers.schemas import FundsSchema, PricesFundSchema
from finex_etf_calc.utils.integrations.finex_etf_adapter import FinexAdapter


class PandasModel:
    @staticmethod
    def get_file_by_name(path_to_file):
        return pd.read_excel(path_to_file)


class FundsLoaderAdapter(PandasModel, FinexAdapter):
    path_to_file = f'{os.path.dirname(os.path.abspath(__file__))}/files'
    path_to_file_to_day = f'{path_to_file}/nav.xlsx'
    path_to_file_to_historical_dynamic = f'{path_to_file}/historical-dynamic.xls'

    @classmethod
    async def create_prices_fund(cls, session: AsyncSession, ticker: str, date: datetime.date, price: float):
        try:
            await PricesFund.create(
                session=session,
                prices=PricesFundSchema(
                    funds_ticker=ticker,
                    price_date=date,
                    price=price,
                ),
            )
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            pass  # TODO добавить лог что не получилось загрузить данное значение и описание ошибки

    @classmethod
    async def check_or_create_fund(cls, session: AsyncSession, ticker: str, currency: float):
        fund = await Funds.get_one_by_params(session, (Funds.ticker == ticker,))
        if fund is None:
            await Funds.create(
                session=session,
                funds=FundsSchema(ticker=ticker, currencies_name=currency),
            )

    async def update_prices_funds(self):
        await self.load_file_from_url(config['FINEX_PRICE_ON_DAY_URL'], self.path_to_file_to_day)
        res = self.get_file_by_name(self.path_to_file_to_day)
        async with scoped_session() as session:
            for ind in res.T:
                ticker = res.T[ind].ticker
                currency = res.T[ind].currency
                date = datetime.date(res.T[ind].date)
                price = res.T[ind].value

                await self.check_or_create_fund(session, ticker, currency)
                await self.create_prices_fund(session, ticker, date, price)

    async def create_prices_by_history(self):
        await self.load_file_from_url(config['FINEX_PRICE_HISTORY_URL'], self.path_to_file_to_historical_dynamic)
        res = self.get_file_by_name(self.path_to_file_to_historical_dynamic)
        async with scoped_session() as session:
            ind = 0
            while ind < res.T.shape[0]:
                ind_first = ind
                ind_second = ind + 1
                ind += 2

                ticker = res.columns.values[ind_second][:4]
                currency = res.columns.values[ind_second][-3:]
                await self.check_or_create_fund(session, ticker, currency)

                dates = res.T.values[ind_first]
                prices = res.T.values[ind_second]
                ind_p = 0
                while ind_p < res.T.shape[1]:
                    if pd.isna(dates[ind_p]):
                        break

                    await self.create_prices_fund(
                        session,
                        ticker,
                        datetime.strptime(dates[ind_p], '%d.%m.%Y').date(),
                        prices[ind_p],
                    )
                    ind_p += 1


funds_loader_adapter = FundsLoaderAdapter()
