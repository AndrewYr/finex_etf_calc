import typing as t
from datetime import date

import sqlalchemy as sa
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import desc
from sqlalchemy.sql import func
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

    prices: Mapped[t.List["PricesCurrency"]] = relationship(lazy="selectin")

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

    ticker: Mapped[str] = mapped_column(sa.String(4), unique=True)
    description: Mapped[str] = mapped_column(sa.String(256))

    currencies: Mapped[t.List["Currencies"]] = relationship(lazy="selectin")
    price: Mapped[t.List["PricesFund"]] = relationship(lazy="selectin")
    deals: Mapped[t.List["Deals"]] = relationship(back_populates="funds", lazy="selectin")

    currencies_id: Mapped[int] = mapped_column(sa.ForeignKey(Currencies.id))

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'Funds':
        rrr = (await session.execute(
            sa.select(Deals.funds_id, func.sum(Deals.count)).where(Deals.type_deal_id == 1).group_by(
                Deals.funds_id).order_by(Deals.funds_id)))
        res = await super().get_one_by_params(cls, session, conditions)
        return res.Funds

    @classmethod
    async def create(cls, session: AsyncSession, data: 'FundsSchema') -> int:
        pass

    @classmethod
    async def get_by_id(cls, session: AsyncSession, fund_id: int) -> int:
        stm = sa.select(cls)
        stream = await session.stream(stm.order_by(cls.id))
        async for row in stream:
            yield row.Funds

    async def get_actual_count(self):
        pass


class PricesFund(BasePrice):
    __tablename__ = PRICES_FUND

    funds_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id))

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_last_by_funds_id(cls, session: AsyncSession, funds_id) -> 'PricesFund':
        res = (await session.execute(sa.select(PricesFund).where(PricesFund.funds_id == funds_id)
                                     .order_by(desc(PricesFund.price_date))))
        return res.first()


class TypesDeals(Base):
    __tablename__ = TYPES_DEALS

    name: Mapped[str] = mapped_column(sa.String(16))
    description: Mapped[str] = mapped_column(sa.String(256))
    deals: Mapped[t.List["Deals"]] = relationship(back_populates="type_deal", lazy="selectin")

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'TypesDeals':
        res = await super().get_one_by_params(cls, session, conditions)
        return res.TypesDeals


class Deals(Base):
    __tablename__ = DEALS

    funds_id: Mapped[int] = mapped_column(sa.ForeignKey(Funds.id))
    funds: Mapped["Funds"] = relationship(back_populates="deals", lazy="selectin")

    type_deal_id: Mapped[int] = mapped_column(sa.ForeignKey(TypesDeals.id))
    type_deal: Mapped["TypesDeals"] = relationship(back_populates="deals", lazy="selectin")

    price: Mapped[float] = mapped_column(sa.Float())
    date_deal: Mapped[date] = mapped_column(sa.Date())
    count: Mapped[int] = mapped_column(sa.BigInteger())

    @classmethod
    async def create(cls, session: AsyncSession, deal: 'DealsSchema') -> int:
        # TODO добавить проверку на наличие количества в БД если речь идет о продаже
        type_deal = await TypesDeals.get_one_by_params(session, (TypesDeals.name == deal.type_deal.name,))
        fund = await Funds.get_one_by_params(session, (Funds.ticker == deal.funds.ticker,))
        new_obj = Deals(
            funds_id=fund.id,
            type_deal_id=type_deal.id,
            price=deal.price,
            date_deal=deal.date_deal,
            count=deal.count,
        )
        session.add(new_obj)
        try:
            await session.flush()
        except Exception as e: # TODO переделать исключение
            print(e)

        return new_obj

    @classmethod
    async def update_deal(cls, session: AsyncSession, deal_id: int, data: '') -> int:
        pass

    @classmethod
    async def get_actual_deals(cls, session: AsyncSession) -> int:
        res_buy = (await session.execute(
            sa.select(cls.funds_id, func.sum(cls.count)).where(cls.type_deal_id == 1).group_by(
                cls.funds_id).order_by(cls.funds_id)))
        res_sell = (await session.execute(
            sa.select(cls.funds_id, func.sum(cls.count)).where(cls.type_deal_id == 1).group_by(
                cls.funds_id).order_by(cls.funds_id)))
        # TODO посчитать разницу между buy и sell по одинаковым funds_id и собрать в отдельную таблицу


        res = (await session.execute(sa.select(cls).group_by(cls.funds_id)))
        res = await PricesFund.get_last_by_funds_id(session)


class PricesCurrency(BasePrice):
    __tablename__ = PRICES_CURRENCIES

    currencies_id: Mapped[int] = mapped_column(sa.ForeignKey(Currencies.id))

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass


class TypesDealsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(None)


class FundsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticker: str = Field(None)


class DealsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(None)
    type_deal: TypesDealsSchema = Field(None)
    funds: FundsSchema = Field(None)
    count: int = Field(None)
    price: float = Field(None)
    date_deal: date = Field(None)
