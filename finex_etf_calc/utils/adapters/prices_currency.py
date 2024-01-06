import datetime

import sqlalchemy as sa

from finex_etf_calc.db.models.funds import PricesCurrency


class PricesCurrencyAdapter(PricesCurrency):
    @classmethod
    async def last_price_currency_on_date(cls, session, currency_name, target_date: datetime.date):
        res = (await session.execute(
            sa.select(
                cls.currencies_name,
                cls.price,
                sa.func.max(cls.price_date).label("max_price_date"),
            ).where(
                sa.and_(
                    cls.price_date <= target_date,
                    cls.currencies_name == currency_name,
                )
            )
            .group_by(cls.currencies_name, cls.price).order_by(sa.desc("max_price_date")).limit(1)
        ))
        return res.first()

