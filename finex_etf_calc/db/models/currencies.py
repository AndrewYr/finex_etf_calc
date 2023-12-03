import sqlalchemy as sa
from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError

from .base import Base


CURRENCIES = 'tcurrencies'


class Currencies(Base):
    __tablename__ = CURRENCIES

    name = sa.Column(sa.String(3))
    code = sa.Column(sa.Integer())

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
        stream = await session.stream(stmt.where(ColumnElement[Currencies.code == code]))
        async for row in stream:
            yield row.Currencies
