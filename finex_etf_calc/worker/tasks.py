from celery.schedules import crontab

from worker import app

app.conf.beat_schedule = {
    'update-etf-price': {
        'task': 'tasks.update_etf_price',
        'schedule': crontab(
            hour='',
            minute='',
        )
    }
}


@app.task(
    name='tasks.update_etf_price'
)
def update_etf_price():
    pass
