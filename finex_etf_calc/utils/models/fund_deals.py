import typing as t
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import Row, func
from sqlalchemy.ext.asyncio import AsyncSession

from finex_etf_calc.db.models.funds import Deals, Funds


class FundDeals:
    @classmethod
    async def get_funds_ticker_and_sum_by_params(
            cls,
            session: AsyncSession,
            conditions: tuple,
    ) -> Sequence[Row[tuple[t.Any, ...] | t.Any]]:
        '''Функция возвращает список funds_ticker и сумму количества штук по переданному условию '''
        res = (await session.execute(
            sa.select(Deals.funds_ticker, func.sum(Deals.count)).where(*conditions).group_by(
                Deals.funds_ticker).order_by(Deals.funds_ticker)))
        return res.all()

    @classmethod
    async def get_actual_count_funds(cls, session: AsyncSession) -> t.List[{}]:  # TODO определить структуру
        res_buy = await cls.get_funds_ticker_and_sum_by_params(session, (Deals.type_deal_id == 1,))
        res_sell = await cls.get_funds_ticker_and_sum_by_params(session, (Deals.type_deal_id == 2,))

        res_lst = []  # TODO переделать на работу с классом
        for i_buy in res_buy:
            fund = await Funds.get_one_by_params(session, (Funds.ticker == i_buy.funds_ticker,))
            if fund is None:
                pass  # TODO подумать над формированием ошибки
                # raise HTTPException(status_code=404, detail=f'{cls.__name__} with params {conditions[0]} not found')
            res_dict = {'funds_ticker': i_buy.funds_ticker, 'count': i_buy.sum, 'currency': fund.currencies_name}
            for i_sell in res_sell:
                if i_buy.funds_ticker == i_sell.funds_ticker:
                    res_dict['count'] = i_buy.sum - i_sell.sum
                    break  # TODO удалить добавленную запись из res_sell
            res_lst.append(res_dict)

        return res_lst
