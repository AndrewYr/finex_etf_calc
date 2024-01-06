from fastapi import APIRouter

from finex_etf_calc.app.celery import app as celery_app

admin_routes = APIRouter()


@admin_routes.post(
    '/funds/prices',
    status_code=200,
    description='Подгружаем историю фондов',
)
async def full_load_prices_funds():
    celery_app.send_task('tasks.full_load_prices_funds')


@admin_routes.post(
    '/currencies/prices',
    status_code=200,
    description='Подгружаем историю валют',
)
async def full_load_prices_currency():
    celery_app.send_task('tasks.full_load_prices_currency')
