from datetime import date
from typing import Any, Tuple

import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy import Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from finex_etf_calc.app.config import config

Model = declarative_base()

Model.metadata.schema = config['DB_SCHEMA']


class Base(Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @staticmethod
    async def get_one_by_params(cls, session: AsyncSession, conditions: tuple) -> Row[tuple[Any, ...] | Any]:
        res = (await session.execute(sa.select(cls).where(*conditions)))
        obj_res = res.one_or_none()
        if obj_res is None:
            raise HTTPException(status_code=404, detail=f'{cls.__name__} with params {conditions[0]} not found')
            # TODO поправить сообщение об ошибке чтобы
        return obj_res


class BasePrice(Base):
    __abstract__ = True

    price_date: Mapped[date] = mapped_column(sa.Date())
    price: Mapped[float] = mapped_column(sa.Float())

    # TODO посмотреть как делаются функции а бстрактных классах, полиморфизм
    @classmethod
    async def create(cls, session: AsyncSession, data: '') -> int:
        pass

    @classmethod
    async def get_by_date(cls, session: AsyncSession, date) -> int:
        pass
