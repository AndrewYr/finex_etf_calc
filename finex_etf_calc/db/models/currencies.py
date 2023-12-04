import typing as t

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, BasePrice
from .funds import Funds

CURRENCIES = 'tcurrencies'
PRICES_CURRENCIES = 'tprices_currency'


class Currencies(Base):
    __tablename__ = CURRENCIES

    name: Mapped[str] = mapped_column(sa.String(3))
    code: Mapped[int] = mapped_column(sa.Integer())

    prices: Mapped[t.List["PricesCurrency"]] = relationship()
    funds_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id.__name__))

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


class PricesCurrency(BasePrice):
    __tablename__ = PRICES_CURRENCIES

    currencies_id: Mapped[int] = mapped_column(sa.ForeignKey(Currencies.id.__name__))

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass
