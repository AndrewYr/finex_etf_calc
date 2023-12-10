from abc import abstractmethod

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from finex_etf_calc.db.engine import get_session


class BaseController:
    def __init__(self, session: sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    @abstractmethod
    async def perform(self, *args, **kwargs):
        pass
