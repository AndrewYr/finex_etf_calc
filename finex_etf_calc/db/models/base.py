import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from finex_etf_calc.app.config import config

Model = declarative_base()

Model.metadata.schema = config['DB_SCHEMA']


class Base(Model):
    __abstract__ = True
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
