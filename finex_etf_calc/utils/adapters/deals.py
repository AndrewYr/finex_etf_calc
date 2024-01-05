import typing as t

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from finex_etf_calc.db.models.funds import Deals, Funds


class DealsAdapter(Deals):
    res_lst = []  # TODO переименовать

    @classmethod
    async def get_actual_count_funds(cls, session: AsyncSession) -> t.List[{}]:  # TODO определить структуру
        res = (await session.execute(
            sa.select(
                cls.funds_ticker,
                func.sum(
                    sa.case(
                        (cls.type_deal_id == 1, cls.count),
                        (cls.type_deal_id == 2, -cls.count),
                        else_=0
                    )
                ),
                Funds.currencies_name,
            ).select_from(
                sa.join(cls, Funds, cls.funds_ticker == Funds.ticker)
            ).where(cls.type_deal_id.in_([1, 2]))
            .group_by(cls.funds_ticker, Funds.currencies_name)
            .order_by(cls.funds_ticker)))
        actual_counts_funds = res.all()

        for fund_count in actual_counts_funds:
            res_dict = {
                'funds_ticker': fund_count.funds_ticker,
                'count': fund_count.sum,
                'currency': fund_count.currencies_name,
            }
            cls.res_lst.append(res_dict)

        return cls.res_lst
