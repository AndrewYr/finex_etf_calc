import asyncio

from celery.schedules import crontab

from finex_etf_calc.worker.controllers import funds_loader_adapter
from worker import app

loop = asyncio.get_event_loop()
app.conf.beat_schedule = {
    'run-update-etf-price': {
        'task': 'tasks.update_etf_price',
        'schedule': crontab(
            hour='11',
            minute='20',
        )
    }
}


@app.task(
    bind=True,
    name='tasks.update_etf_price',
    retry_backoff=60,
    retry_jitter=False,
    retry_kwargs={
        'max_retries': 10
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
        'max_retries': 10
    }
)
def first_load_prices(*args, **kwargs):
    loop.run_until_complete(funds_loader_adapter.create_prices_by_history())


@app.task(
    bind=True,
    name='tasks.update_prices_currency',
    retry_backoff=60,
    retry_jitter=False,
    retry_kwargs={
        'max_retries': 10
    }
)
def update_prices_currency(*args, **kwargs):
    loop.run_until_complete()


