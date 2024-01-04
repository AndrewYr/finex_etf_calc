import typing as t
from datetime import date
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import desc, Row, UniqueConstraint, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import relationship, Mapped, mapped_column

from finex_etf_calc.db.models import Base, BasePrice

FUNDS = 'tfunds'
PRICES_FUND = 'tprices_fund'
DEALS = 'tdeals'
TYPES_DEALS = 'ttypes_deal'
CURRENCIES = 'tcurrencies'
PRICES_CURRENCIES = 'tprices_currency'


class Currencies(Base):
    __tablename__ = CURRENCIES

    name: Mapped[str] = mapped_column(sa.String(3), unique=True)
    code: Mapped[int] = mapped_column(sa.Integer(), unique=True)
    description: Mapped[str] = mapped_column(sa.String(256), nullable=True)

    prices: Mapped[t.List["PricesCurrency"]] = relationship(lazy="selectin")

    def __init__(self, name, code):
        self.name = name
        self.code = code

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'Currencies':
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj = res.one_or_none()
        return obj.Currencies

    @classmethod
    async def create(cls, session: AsyncSession, data: 'CurrenciesSchema') -> int:
        currency = Currencies(name=data.name, code=data.code)
        session.add(currency)
        try:
            await session.flush()
        except OperationalError:
            await session.rollback()


class PricesCurrency(BasePrice):
    __tablename__ = PRICES_CURRENCIES

    currencies_name: Mapped[str] = mapped_column(sa.ForeignKey(Currencies.name))

    _table_args__ = (UniqueConstraint('currencies_name', 'price_date', name='unique_prices_currency'),)

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'PricesCurrency':
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj = res.one_or_none()
        return obj.PricesCurrency

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass


class Funds(Base):
    __tablename__ = FUNDS

    ticker: Mapped[str] = mapped_column(sa.String(4), unique=True)
    description: Mapped[str] = mapped_column(sa.String(256), nullable=True)

    currencies: Mapped[t.List["Currencies"]] = relationship(lazy="selectin")
    price: Mapped[t.List["PricesFund"]] = relationship(lazy="selectin")
    deals: Mapped[t.List["Deals"]] = relationship(back_populates="funds", lazy="selectin")

    currencies_name: Mapped[str] = mapped_column(sa.ForeignKey(Currencies.name))

    def __init__(self, ticker, currencies_name):
        self.ticker = ticker
        self.currencies_name = currencies_name

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'Funds':
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj = res.one_or_none()
        return obj.Funds

    @classmethod
    async def create(cls, session: AsyncSession, funds: 'FundsSchema') -> 'Funds':
        new_onj = Funds(
            ticker=funds.ticker,
            currencies_name=funds.currencies_name,
        )
        session.add(new_onj)
        try:
            await session.flush()
        except OperationalError:
            await session.rollback()

        return new_onj


class PricesFund(BasePrice):
    __tablename__ = PRICES_FUND

    funds_ticker: Mapped[str] = mapped_column(sa.ForeignKey(Funds.ticker))

    _table_args__ = (UniqueConstraint('funds_ticker', 'price_date', name='unique_prices_fund'),)

    def __init__(self, funds_ticker, price_date, price):
        self.funds_ticker = funds_ticker
        self.price_date = price_date
        self.price = price

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'PricesFund':
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj = res.one_or_none()
        return obj.PricesFund

    @classmethod
    async def create(cls, session: AsyncSession, prices: 'PricesFundSchema') -> 'PricesFund':
        new_obj = PricesFund(
            funds_ticker=prices.funds_ticker,
            price_date=prices.price_date,
            price=prices.price,
        )
        session.add(new_obj)
        try:
            await session.flush()
        except OperationalError:
            await session.rollback()

        return new_obj


class TypesDeals(Base):
    __tablename__ = TYPES_DEALS

    name: Mapped[str] = mapped_column(sa.String(16))
    description: Mapped[str] = mapped_column(sa.String(256), nullable=True)
    deals: Mapped[t.List["Deals"]] = relationship(back_populates="type_deal", lazy="selectin")

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'TypesDeals':
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj = res.one_or_none()
        return obj.TypesDeals

    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass


class Deals(Base):
    __tablename__ = DEALS

    funds_ticker: Mapped[str] = mapped_column(sa.ForeignKey(Funds.ticker))
    funds: Mapped["Funds"] = relationship(back_populates="deals", lazy="selectin")

    type_deal_id: Mapped[int] = mapped_column(sa.ForeignKey(TypesDeals.id))
    type_deal: Mapped["TypesDeals"] = relationship(back_populates="deals", lazy="selectin")

    price: Mapped[float] = mapped_column(sa.Float())
    date_deal: Mapped[date] = mapped_column(sa.Date())
    count: Mapped[int] = mapped_column(sa.Integer())

    def __init__(self, funds_ticker, type_deal_id, price, date_deal, count):
        self.funds_ticker = funds_ticker
        self.type_deal_id = type_deal_id
        self.price = price
        self.date_deal = date_deal
        self.count = count

    @classmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> 'Deals':
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj = res.one_or_none()
        return obj.Deals

    @classmethod
    async def create(cls, session: AsyncSession, deal: 'DealsSchema') -> 'Deals':
        # TODO добавить проверку на наличие количества в БД если речь идет о продаже
        type_deal = await TypesDeals.get_one_by_params(session, (TypesDeals.name == deal.type_deal.name,))
        fund = await Funds.get_one_by_params(session, (Funds.ticker == deal.funds.ticker,))
        if type_deal is None or fund is None:
            pass  # TODO подумать как обработкать не найденные значения
            # raise HTTPException(status_code=404, detail=f'{cls.__name__} with params {conditions[0]} not found')

        new_obj = Deals(
            funds_ticker=fund.ticker,
            type_deal_id=type_deal.id,
            price=deal.price,
            date_deal=deal.date_deal,
            count=deal.count,
        )
        session.add(new_obj)
        try:
            await session.flush()
        except OperationalError:
            await session.rollback()

        return new_obj
