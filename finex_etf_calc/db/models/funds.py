import typing as t
from datetime import date

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped, mapped_column

from finex_etf_calc.db.models.currencies import Currencies

from .base import Base, BasePrice

FUNDS = 'tfunds'
PRICES_FUND = 'tprices_fund'
DEALS = 'tdeals'


class Funds(Base):
    __tablename__ = FUNDS

    ticker: Mapped[str] = mapped_column(sa.String(4))
    description: Mapped[str] = mapped_column(sa.String(256))

    currencies: Mapped[t.List["Currencies"]] = relationship()
    price: Mapped[t.List["PricesFund"]] = relationship()
    deals: Mapped[t.List["Deals"]] = relationship(back_populates="funds")

    @classmethod
    async def create(cls, session: AsyncSession, data: 'FundsSchema') -> int:
        pass

    @classmethod
    async def get_by_id(cls, session: AsyncSession, fund_id: int) -> int:
        stm = sa.select(cls)
        stream = await session.stream(stm.order_by(cls.id))
        async for row in stream:
            yield row.Funds


class PricesFund(BasePrice):
    __tablename__ = PRICES_FUND

    parent_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id.__name__))

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass


class Deals(Base):
    __tablename__ = DEALS

    funds_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id.__name__))
    funds: Mapped["Funds"] = relationship(back_populates="deals")

    amount: Mapped[float] = mapped_column(sa.Float())
    deal_date: Mapped[date] = mapped_column(sa.Date())
    count: Mapped[int] = mapped_column(sa.BigInteger())

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def update_deal(cls, session: AsyncSession, deal_id: int, data: '') -> int:
        pass
