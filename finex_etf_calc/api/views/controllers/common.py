from abc import abstractmethod

from fastapi import Depends
from sqlalchemy.orm import sessionmaker


class BaseController:
    def __init__(self, session: sessionmaker = Depends()):
        self.async_session = session

    @abstractmethod
    async def perform(self, data):
        pass
