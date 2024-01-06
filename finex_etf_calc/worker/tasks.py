import time
import asyncio

from celery.schedules import crontab

from finex_etf_calc.worker.controllers import funds_loader_adapter, currencies_loader_adapter
from worker import app

loop = asyncio.get_event_loop()
app.conf.beat_schedule = {
    'run-update-etf-price': {
        'task': 'tasks.update_etf_price_today',
        'schedule': crontab(
            hour='00',
            minute='05',
        )
    },
    'run-update-prices-currency': {
        'task': 'tasks.update_prices_currency_today',
        'schedule': crontab(
            hour='00',
            minute='05',
        )
    }
}


@app.task(
    name='tasks.update_etf_price_today',
)
def update_etf_price_task(*args, **kwargs):
    loop.run_until_complete(funds_loader_adapter.update_prices_funds())


@app.task(
    name='tasks.update_prices_currency_today',
)
def update_prices_currency_task(*args, **kwargs):
    loop.run_until_complete(currencies_loader_adapter.update_prices_currency())


@app.task(
    name='tasks.full_load_prices_funds',
)
def full_load_prices_funds_task(*args, **kwargs):
    start_time = time.time()
    loop.run_until_complete(funds_loader_adapter.load_prices_funds())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Elapsed time: ', elapsed_time)


@app.task(
    name='tasks.full_load_prices_currency',
)
def full_load_prices_currency_task(*args, **kwargs):
    loop.run_until_complete(currencies_loader_adapter.load_all_prices_currency())

