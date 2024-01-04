from datetime import date
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import desc, Row
from sqlalchemy.ext.asyncio import AsyncSession

from finex_etf_calc.db.models.funds import PricesFund


class PricesFundAdapter(PricesFund):

    @classmethod
    async def get_actual_price_by_funds_ticker(
            cls,
            session: AsyncSession,
            funds_ticker,
    ) -> Sequence[Row[tuple[float, date]]]:
        stmt = (
            sa.select(PricesFund.price)
            .where(PricesFund.funds_ticker == funds_ticker)
            .order_by(desc(PricesFund.price_date))
            .limit(1)
            .with_only_columns(PricesFund.price_date)
        )
        result = await session.execute(stmt)
        latest_price_date = result.scalar()

        stmt = (
            sa.select(PricesFund.price, PricesFund.price_date)
            .where((PricesFund.funds_ticker == funds_ticker) & (PricesFund.price_date == latest_price_date))
            .with_only_columns(PricesFund.price, PricesFund.price_date)
        )
        result = await session.execute(stmt)
        return result.one_or_none()

    @classmethod
    async def fill_actual_price_funds(cls, session: AsyncSession, list_funds):
        # TODO округление перенести на уровень модели сериализации
        for fund in list_funds:
            resp_price = await cls.get_actual_price_by_funds_ticker(session, fund['funds_ticker'])
            fund['price'] = round(resp_price.price, 2)
            fund['price_date'] = resp_price.price_date
            try:
                fund['result'] = round(fund['price'] * fund['count'], 2)
            except TypeError as e:
                fund['result'] = None
