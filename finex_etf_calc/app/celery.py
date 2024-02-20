import celery

from finex_etf_calc.app.config import config

app = celery.Celery(
    'finex_etf_calc',
    broker=config.CELERY_URLS,
    broker_connection_retry_on_startup=True,
    include=[
        'finex_etf_calc.worker.tasks'
    ],
)
app.conf.update(
    timezone='Europe/Moscow',
    enable_utc=True,
)
