import asyncio
import os
from datetime import datetime, date

import numpy as np
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from finex_etf_calc.app.config import config
from finex_etf_calc.db.engine import scoped_session
from finex_etf_calc.db.models.funds import Funds, PricesFund, Currencies, PricesCurrency
from finex_etf_calc.api.views.serializers.schemas import FundsSchema, PricesFundSchema, PricesCurrencySchema
from finex_etf_calc.utils.constants import CurrenciesNames
from finex_etf_calc.utils.integrations.finex_etf_adapter import FinexAdapter
from finex_etf_calc.utils.integrations.cbr_adapter import CBRAdapter


class PandasModel:
    @staticmethod
    def get_file_by_name(path_to_file):
        return pd.read_excel(path_to_file)


class FundsLoaderAdapter(PandasModel, FinexAdapter):
    path_to_file = f'{os.path.dirname(os.path.abspath(__file__))}/files'
    path_to_file_to_day = f'{path_to_file}/nav.xlsx'
    path_to_file_to_historical_dynamic = f'{path_to_file}/historical-dynamic.xls'

    @classmethod
    async def check_or_create_prices_fund(cls, session: AsyncSession, ticker: str, date_price: datetime.date, price: float):
        prices_fund = await PricesFund.get_one_by_params(
            session,
            (PricesFund.funds_ticker == ticker, PricesFund.price_date == date_price,),
        )
        if prices_fund is None:
            try:
                await PricesFund.create(
                    session=session,
                    prices=PricesFundSchema(
                        funds_ticker=ticker,
                        price_date=date_price,
                        price=price,
                    ),
                )
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                pass  # TODO добавить лог что не получилось загрузить данное значение и описание ошибки

    @classmethod
    async def check_or_create_fund(cls, session: AsyncSession, ticker: str, currency: float):
        stmt = insert(Funds).values(
            ticker=ticker,
            currencies_name=currency,
        ).on_conflict_do_nothing(index_elements=[Funds.ticker])

        await session.execute(stmt)
        await session.commit()

    async def update_prices_funds(self):
        await self.load_file_from_url(config.FINEX_PRICE_ON_DAY_URL, self.path_to_file_to_day)
        res = self.get_file_by_name(self.path_to_file_to_day)
        async with scoped_session() as session:
            for ind in res.T:
                ticker = res.T[ind].ticker
                currency = res.T[ind].currency
                date_res = datetime.date(res.T[ind].date)
                price = res.T[ind].value

                await self.check_or_create_fund(session, ticker, currency)
                await self.check_or_create_prices_fund(session, ticker, date_res, price)

    async def load_prices_funds(self):
        await self.load_file_from_url(config.FINEX_PRICE_HISTORY_URL, self.path_to_file_to_historical_dynamic)
        res = self.get_file_by_name(self.path_to_file_to_historical_dynamic)
        split_data = np.array_split(res, 4)

        tasks = [self.process_data_part(part) for part in split_data]
        await asyncio.gather(*tasks)

    async def process_data_part(self, data_part):  # TODO переназвать функцию посмотреть как можно оптимизировать код
        async with scoped_session() as session:
            ind = 0
            while ind < data_part.T.shape[0]:
                ind_first = ind
                ind_second = ind + 1
                ind += 2

                ticker = data_part.columns.values[ind_second][:4]
                currency = data_part.columns.values[ind_second][-3:]
                await self.check_or_create_fund(session, ticker, currency)

                dates = data_part.T.values[ind_first]
                prices = data_part.T.values[ind_second]
                ind_p = 0
                while ind_p < data_part.T.shape[1]:
                    if pd.isna(dates[ind_p]):
                        break

                    await self.check_or_create_prices_fund(
                        session,
                        ticker,
                        datetime.strptime(dates[ind_p], '%d.%m.%Y').date(),
                        prices[ind_p],
                    )
                    ind_p += 1


class CurrenciesLoaderAdapter(CBRAdapter):
    @staticmethod
    async def first_last_date_currencies(session):
        res = (await session.execute(
            sa.select(
                Currencies.name,
                Currencies.code_cbr,
                func.min(PricesFund.price_date).label("start_date"),
                func.max(PricesFund.price_date).label("end_date"),
            ).where(Currencies.name != CurrenciesNames.RUB).group_by(Currencies.name, Currencies.code_cbr)))
        list_first_last_date_currencies = res.all()
        return list_first_last_date_currencies

    @classmethod
    async def check_or_create_prices_currency(
            cls,
            session: AsyncSession,
            currency_name: str,
            date_price: datetime.date,
            price: float,
    ):
        prices_currency = await PricesCurrency.get_one_by_params(
            session,
            (PricesCurrency.currencies_name == currency_name, PricesCurrency.price_date == date_price,),
        )
        if prices_currency is None:
            try:
                await PricesCurrency.create(
                    session=session,
                    prices=PricesCurrencySchema(
                        currency_name=currency_name,
                        price_date=date_price,
                        price=price,
                    ),
                )
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                pass  # TODO добавить лог что не получилось загрузить данное значение и описание ошибки

    async def load_all_prices_currency(self):
        async with scoped_session() as session:
            lst_currencies = await self.first_last_date_currencies(session)
            for currency in lst_currencies:
                prices_currency = self.get_curs_dynamic(
                    currency.start_date.strftime('%Y-%m-%d'),
                    currency.end_date.strftime('%Y-%m-%d'),
                    currency.code_cbr,
                )

                for price in prices_currency:
                    await self.check_or_create_prices_currency(
                        session,
                        currency.name,
                        datetime.strptime(price['CursDate'], '%Y-%m-%dT%H:%M:%S%z').date(),
                        price['VunitRate'],
                    )

    async def update_prices_currency(self):
        prices_currency_response, date_response = self.get_curs_on_date(
            date.today().strftime('%Y-%m-%d')
        )
        async with scoped_session() as session:
            for price in prices_currency_response:
                if price['VchCode'] in CurrenciesNames.get_attributes():
                    await self.check_or_create_prices_currency(
                        session,
                        price['VchCode'],
                        date_response,
                        price['VunitRate'],
                    )


funds_loader_adapter = FundsLoaderAdapter()
currencies_loader_adapter = CurrenciesLoaderAdapter()
