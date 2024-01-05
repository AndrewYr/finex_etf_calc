import asyncio

from celery.schedules import crontab

from finex_etf_calc.worker.controllers import funds_loader_adapter, currencies_loader_adapter
from worker import app

loop = asyncio.get_event_loop()
# app.conf.beat_schedule = {
#     'run-update-etf-price': {
#         'task': 'tasks.load_prices_currency',
#         'schedule': crontab(
#             hour='19',
#             minute='03',
#         )
#     }
# }


@app.task(
    bind=True,
    name='tasks.update_etf_price',
    retry_backoff=60,
    retry_jitter=False,
    retry_kwargs={
        'max_retries': 3
    }
)
def update_etf_price(*args, **kwargs):
    loop.run_until_complete(funds_loader_adapter.update_prices_funds())


@app.task(
    bind=True,
    name='tasks.first_load',
    retry_backoff=60,
    retry_jitter=False,
    retry_kwargs={
        'max_retries': 3
    }
)
def first_load_prices(*args, **kwargs):
    loop.run_until_complete(funds_loader_adapter.create_prices_by_history())


@app.task(
    name='tasks.load_prices_currency',
)
def load_prices_currency(*args, **kwargs):
    loop.run_until_complete(currencies_loader_adapter.load_all_prices_currency())


