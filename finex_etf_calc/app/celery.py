import celery.signals

from finex_etf_calc.app.config import config

app = celery.Celery(
    'finex_etf_calc',
    broker=config['CELERY_URLS'],
    include=[
        'finex_etf_calc.worker.tasks'
    ],
)
app.conf.timezone = config['Europe/Moscow']
