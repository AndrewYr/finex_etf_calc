"""initial

Revision ID: a1f4c48b8c7a
Revises: 
Create Date: 2023-12-17 19:17:10.225167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from finex_etf_calc.app.config import config

# revision identifiers, used by Alembic.
revision: str = 'a1f4c48b8c7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tcurrencies',
    sa.Column('name', sa.String(length=3), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('code_cbr', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name'),
    schema=config.DB_SCHEMA
    )
    op.create_table('ttypes_deal',
    sa.Column('name', sa.String(length=16), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=config.DB_SCHEMA
    )
    op.create_table('tfunds',
    sa.Column('ticker', sa.String(length=4), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('currencies_name', sa.String(length=3), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['currencies_name'], [f'{config.DB_SCHEMA}.tcurrencies.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ticker'),
    schema=config.DB_SCHEMA
    )
    op.create_table('tprices_currency',
    sa.Column('currencies_name', sa.String(length=3), nullable=False),
    sa.Column('price_date', sa.Date(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['currencies_name'], [f'{config.DB_SCHEMA}.tcurrencies.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint("currencies_name", "price_date", name="unique_prices_currency"),
    schema=config.DB_SCHEMA
    )
    op.create_table('tdeals',
    sa.Column('funds_ticker', sa.String(length=4), nullable=False),
    sa.Column('type_deal_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('date_deal', sa.Date(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['funds_ticker'], [f'{config.DB_SCHEMA}.tfunds.ticker'], ),
    sa.ForeignKeyConstraint(['type_deal_id'], [f'{config.DB_SCHEMA}.ttypes_deal.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=config.DB_SCHEMA
    )
    op.create_table('tprices_fund',
    sa.Column('funds_ticker', sa.String(length=4), nullable=False),
    sa.Column('price_date', sa.Date(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['funds_ticker'], [f'{config.DB_SCHEMA}.tfunds.ticker'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint("funds_ticker", "price_date", name="unique_prices_fund"),
    schema=config.DB_SCHEMA
    )
    # ### end Alembic commands ###
    meta = sa.MetaData()
    ttypes_deal = sa.Table(
        'ttypes_deal',
        meta,
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('id', sa.Integer),
        schema=config.DB_SCHEMA
    )
    op.bulk_insert(
        ttypes_deal,
        [
            {
                'name': 'buy',
                'description': 'Покупка'
            },
            {
                'name': 'sell',
                'description': 'Продажа'
            }
        ]
    )
    tcurrencies = sa.Table(
        'tcurrencies',
        meta,
        sa.Column('name', sa.String),
        sa.Column('code', sa.Integer),
        sa.Column('description', sa.String),
        sa.Column('id', sa.Integer),
        schema=config.DB_SCHEMA
    )
    op.bulk_insert(
        tcurrencies,
        [
            {
                'name': 'USD',
                'code': 840,
                'code_cbr': 'R01235',
                'description': 'Доллар США'
            },
            {
                'name': 'RUB',
                'code': 643,
                'description': 'Российский рубль'
            },
            {
                'name': 'KZT',
                'code': 398,
                'code_cbr': 'R01335',
                'description': 'Тенге'
            },
            {
                'name': 'EUR',
                'code': 978,
                'code_cbr': 'R01239',
                'description': 'Евро'
            }
        ]
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tprices_fund', schema=config.DB_SCHEMA)
    op.drop_table('tdeals', schema=config.DB_SCHEMA)
    op.drop_table('tprices_currency', schema=config.DB_SCHEMA)
    op.drop_table('tfunds', schema=config.DB_SCHEMA)
    op.drop_table('ttypes_deal', schema=config.DB_SCHEMA)
    op.drop_table('tcurrencies', schema=config.DB_SCHEMA)
    # ### end Alembic commands ###
