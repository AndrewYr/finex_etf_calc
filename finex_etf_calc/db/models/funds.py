import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from finex_etf_calc.db.models.currencies import Currencies

from .base import Base


FUNDS = 'tfunds'
PRICES = 'tprices'
DEALS = 'tdeals'


class Funds(Base):
    __tablename__ = FUNDS

    ticker = sa.Column(sa.String(4))
    description = sa.Column(sa.String(256))
    currencies_id = sa.Column(FUNDS, sa.BigInteger(), sa.ForeignKey(Currencies.id))
    currencies = relationship(Currencies)

    @classmethod
    async def create(cls, session: AsyncSession, data: 'FundsSchema') -> int:
        pass

    @classmethod
    async def get_by_id(cls, session: AsyncSession, fund_id: int) -> int:
        stm = sa.select(cls)
        stream = await session.stream(stm.order_by(cls.id))
        async for row in stream:
            yield row.Funds


class Prices(Base):
    __tablename__ = PRICES

    funds_id = sa.Column(FUNDS, sa.BigInteger(), sa.ForeignKey(Funds.id))
    funds = relationship(Funds)
    price_datetime = sa.Column(sa.DateTime())
    price = sa.Column(sa.Float())

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass


class Deals(Base):
    __tablename__ = DEALS

    funds_id = sa.Column(FUNDS, sa.BigInteger(), sa.ForeignKey(Funds.id))
    funds = relationship(Funds)
    amount = sa.Column(sa.Float())
    deal_date = sa.Column(sa.DateTime())
    count = sa.Column(sa.BigInteger())

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def update_deal(cls, session: AsyncSession, deal_id: int, data: '') -> int:
        pass
