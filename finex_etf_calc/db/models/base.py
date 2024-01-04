from abc import abstractmethod, ABC
from datetime import date
from typing import Any

import sqlalchemy as sa
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from finex_etf_calc.app.config import config

Model = declarative_base()

Model.metadata.schema = config['DB_SCHEMA']


# TODO посмотреть как добавить ABC в Base
class Base(Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_one_by_params(self, session: AsyncSession, conditions: tuple) -> Row[tuple[Any, ...] | None]:
        pass


class BasePrice(Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    price_date: Mapped[date] = mapped_column(sa.Date())
    price: Mapped[float] = mapped_column(sa.Float())

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass
