import typing as t
from fastapi import APIRouter

admin_routes = APIRouter()

# TODO подумать нужна ли админка заполнения чего либо
@admin_routes.post(
    '/funds',
    response_model=t.List[dict],
    status_code=201,
    description='Создает недостающие фонды и заполняет их цену',
)
async def create_funds():
    pass
