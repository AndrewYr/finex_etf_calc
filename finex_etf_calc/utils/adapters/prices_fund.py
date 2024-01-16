from typing import Sequence, Any

import sqlalchemy as sa
from sqlalchemy import desc, Row, func
from sqlalchemy.ext.asyncio import AsyncSession

from finex_etf_calc.db.models.funds import PricesFund


class PricesFundAdapter(PricesFund):

    @classmethod
    async def get_actual_price_by_funds_tickers(
            cls,
            session: AsyncSession,
            funds_ticker_list,
    ) -> Sequence[Row[tuple[Any, Any, Any]]]:
        stmt = (
            sa.select(cls.price)
            .where(cls.funds_ticker.in_(funds_ticker_list))
            .order_by(desc(cls.price_date))
            .limit(1)
            .with_only_columns(cls.price_date)
        )
        result = await session.execute(stmt)
        latest_price_date = result.scalar()

        subquery = (
            sa.select(
                cls.funds_ticker,
                func.max(cls.price_date).label("max_date")
            )
            .where(cls.funds_ticker.in_(funds_ticker_list))
            .group_by(cls.funds_ticker)
            .subquery()
        )

        stmt = (
            sa.select(cls.price, cls.price_date, cls.funds_ticker)
            .join(subquery, sa.and_(
                cls.funds_ticker == subquery.c.funds_ticker,
                cls.price_date == subquery.c.max_date
            ))
            .where(cls.price_date <= latest_price_date)
            .order_by(desc(cls.price_date))
        )
        result = await session.execute(stmt)
        return result.all()

    @classmethod
    async def get_actual_price_funds(cls, session: AsyncSession, list_funds):  # TODO добавить описание ответа
        resp_price = await cls.get_actual_price_by_funds_tickers(session, [_['funds_ticker'] for _ in list_funds])
        return [
            {
                'price': item.price,
                'price_date': item.price_date,
                'funds_ticker': item.funds_ticker,
            } for item in resp_price
        ]
