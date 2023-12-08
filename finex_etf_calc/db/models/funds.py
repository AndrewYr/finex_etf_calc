import typing as t
from datetime import date

import sqlalchemy as sa
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, BasePrice

FUNDS = 'tfunds'
PRICES_FUND = 'tprices_fund'
DEALS = 'tdeals'
TYPES_DEALS = 'ttypes_deal'
CURRENCIES = 'tcurrencies'
PRICES_CURRENCIES = 'tprices_currency'


class Currencies(Base):
    __tablename__ = CURRENCIES

    name: Mapped[str] = mapped_column(sa.String(3))
    code: Mapped[int] = mapped_column(sa.Integer())
    description: Mapped[str] = mapped_column(sa.String(256))

    prices: Mapped[t.List["PricesCurrency"]] = relationship()

    @classmethod
    async def create(cls, session: AsyncSession, data: 'CurrenciesSchema') -> int:
        currency = Currencies(name=data.name, code=data.code)
        session.add(currency)
        try:
            await session.flush()
        except OperationalError:
            await session.rollback()

    @classmethod
    async def get_by_code(cls, session: AsyncSession, code: int) -> int:
        stmt = sa.select(cls)
        stream = await session.stream(stmt.where(sa.ColumnElement[Currencies.code == code]))
        async for row in stream:
            yield row.Currencies


class Funds(Base):
    __tablename__ = FUNDS

    ticker: Mapped[str] = mapped_column(sa.String(4))
    description: Mapped[str] = mapped_column(sa.String(256))

    currencies: Mapped[t.List["Currencies"]] = relationship()
    price: Mapped[t.List["PricesFund"]] = relationship()
    deals: Mapped[t.List["Deals"]] = relationship(back_populates="funds")

    currencies_id: Mapped[int] = mapped_column(sa.ForeignKey(Currencies.id))

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

    parent_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id))

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass


class TypesDeals(Base):
    __tablename__ = TYPES_DEALS

    name: Mapped[str] = mapped_column(sa.String(16))
    description: Mapped[str] = mapped_column(sa.String(256))


class Deals(Base):
    __tablename__ = DEALS

    funds_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id))
    funds: Mapped["Funds"] = relationship(back_populates="deals")

    type_deal_id: Mapped[int] = mapped_column(sa.ForeignKey(TypesDeals.id))

    price: Mapped[float] = mapped_column(sa.Float())
    deal_date: Mapped[date] = mapped_column(sa.Date())
    count: Mapped[int] = mapped_column(sa.BigInteger())

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def update_deal(cls, session: AsyncSession, deal_id: int, data: '') -> int:
        pass


class PricesCurrency(BasePrice):
    __tablename__ = PRICES_CURRENCIES

    currencies_id: Mapped[int] = mapped_column(sa.ForeignKey(Currencies.id))

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass


class DealsSchema(BaseModel):
    class Config:
        from_attributes = True

    id: int = Field(None)
    type: str = Field(None)
    # type_id: int = Field(..., description='тип сделки id', examples=[1, 2])
    fund: str = Field(None)
    count: int = Field(None)
    price: float = Field(None)
    date_deal: date = Field(None)
