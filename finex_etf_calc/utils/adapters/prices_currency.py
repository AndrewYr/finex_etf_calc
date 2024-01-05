import datetime

import sqlalchemy as sa

from finex_etf_calc.db.models.funds import PricesCurrency, Currencies


class PricesCurrencyAdapter:
    @staticmethod
    async def last_price_currency_on_date(session, currency_name, target_date: datetime.date):
        res = (await session.execute(
            sa.select(
                PricesCurrency.currencies_name,
                PricesCurrency.price,
                sa.func.max(PricesCurrency.price_date).label("max_price_date"),
            ).where(
                sa.and_(
                    PricesCurrency.price_date <= target_date,
                    PricesCurrency.currencies_name == currency_name,
                )
            )
            .group_by(PricesCurrency.currencies_name, PricesCurrency.price).order_by(sa.desc("max_price_date")).limit(1)
        ))
        return res.first()

