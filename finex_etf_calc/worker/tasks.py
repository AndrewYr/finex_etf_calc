import asyncio

from celery.schedules import crontab

from finex_etf_calc.worker.controllers import funds_loader_adapter, currencies_loader_adapter
from worker import app

loop = asyncio.get_event_loop()
# app.conf.beat_schedule = {
#     'run-update-etf-price': {
#         'task': 'tasks.update_prices_currency_today',
#         'schedule': crontab(
#             hour='13',
#             minute='26',
#         )
#     }
# }


@app.task(
    bind=True,
    name='tasks.update_etf_price_today',
    retry_backoff=60,
    retry_jitter=False,
    retry_kwargs={
        'max_retries': 3
    }
)
def update_etf_price_task(*args, **kwargs):
    loop.run_until_complete(funds_loader_adapter.update_prices_funds())


@app.task(
    bind=True,
    name='tasks.full_load_prices_funds',
    retry_backoff=60,
    retry_jitter=False,
    retry_kwargs={
        'max_retries': 3
    }
)
def full_load_prices_funds_task(*args, **kwargs):
    loop.run_until_complete(funds_loader_adapter.full_load_prices_funds())


@app.task(
    name='tasks.full_load_prices_currency',
)
def full_load_prices_currency_task(*args, **kwargs):
    loop.run_until_complete(currencies_loader_adapter.create_prices_currency())


@app.task(
    name='tasks.update_prices_currency_today',
)
def update_prices_currency_task(*args, **kwargs):
    loop.run_until_complete(currencies_loader_adapter.update_prices_currency())


